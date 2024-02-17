import { createEffect, createRoot, createSignal } from "solid-js";
import { name, version } from "../package.json";

/**
 * @typedef AnyWidget
 * @prop initialize {import("@anywidget/types").Initialize}
 * @prop render {import("@anywidget/types").Render}
 */

/**
 *  @typedef AnyWidgetModule
 *  @prop render {import("@anywidget/types").Render=}
 *  @prop default {AnyWidget | (() => AnyWidget | Promise<AnyWidget>)=}
 */

/**
 * @param {any} condition
 * @param {string} message
 * @returns {asserts condition}
 */
function assert(condition, message) {
	if (!condition) throw new Error(message);
}

/**
 * @param {string} str
 * @returns {str is "https://${string}" | "http://${string}"}
 */
function is_href(str) {
	return str.startsWith("http://") || str.startsWith("https://");
}

/**
 * @param {string} href
 * @param {string} anywidget_id
 * @returns {Promise<void>}
 */
async function load_css_href(href, anywidget_id) {
	/** @type {HTMLLinkElement | null} */
	let prev = document.querySelector(`link[id='${anywidget_id}']`);

	// Adapted from https://github.com/vitejs/vite/blob/d59e1acc2efc0307488364e9f2fad528ec57f204/packages/vite/src/client/client.ts#L185-L201
	// Swaps out old styles with new, but avoids flash of unstyled content.
	// No need to await the load since we already have styles applied.
	if (prev) {
		let newLink = /** @type {HTMLLinkElement} */ (prev.cloneNode());
		newLink.href = href;
		newLink.addEventListener("load", () => prev?.remove());
		newLink.addEventListener("error", () => prev?.remove());
		prev.after(newLink);
		return;
	}

	return new Promise((resolve) => {
		let link = Object.assign(document.createElement("link"), {
			rel: "stylesheet",
			href,
			onload: resolve,
		});
		document.head.appendChild(link);
	});
}

/**
 * @param {string} css_text
 * @param {string} anywidget_id
 * @returns {void}
 */
function load_css_text(css_text, anywidget_id) {
	/** @type {HTMLStyleElement | null} */
	let prev = document.querySelector(`style[id='${anywidget_id}']`);
	if (prev) {
		// replace instead of creating a new DOM node
		prev.textContent = css_text;
		return;
	}
	let style = Object.assign(document.createElement("style"), {
		id: anywidget_id,
		type: "text/css",
	});
	style.appendChild(document.createTextNode(css_text));
	document.head.appendChild(style);
}

/**
 * @param {string | undefined} css
 * @param {string} anywidget_id
 * @returns {Promise<void>}
 */
async function load_css(css, anywidget_id) {
	if (!css || !anywidget_id) return;
	if (is_href(css)) return load_css_href(css, anywidget_id);
	return load_css_text(css, anywidget_id);
}

/**
 * @param {string} esm
 * @returns {Promise<AnyWidgetModule>}
 */
async function load_esm(esm) {
	if (is_href(esm)) {
		return import(/* webpackIgnore: true */ esm);
	}
	let url = URL.createObjectURL(new Blob([esm], { type: "text/javascript" }));
	let widget;
	try {
		widget = await import(/* webpackIgnore: true */ url);
	} catch (e) {
		console.error(e);
	}
	URL.revokeObjectURL(url);
	return widget;
}

function warn_render_deprecation() {
	console.warn(`\
[anywidget] Deprecation Warning. Direct export of a 'render' will likely be deprecated in the future. To migrate ...

Remove the 'export' keyword from 'render'
-----------------------------------------

export function render({ model, el }) { ... }
^^^^^^

Create a default export that returns an object with 'render'
------------------------------------------------------------

function render({ model, el }) { ... }
         ^^^^^^
export default { render }
                 ^^^^^^

To learn more, please see: https://github.com/manzt/anywidget/pull/395
`);
}

/**
 * @param {string} esm
 * @returns {Promise<AnyWidget>}
 */
async function load_widget(esm) {
	let mod = await load_esm(esm);
	if (mod.render) {
		warn_render_deprecation();
		return {
			async initialize() {},
			render: mod.render,
		};
	}
	assert(
		mod.default,
		`[anywidget] module must export a default function or object.`,
	);
	let widget = typeof mod.default === "function"
		? await mod.default()
		: mod.default;
	return widget;
}

/**
 * This is a trick so that we can cleanup event listeners added
 * by the user-defined function.
 */
let INITIALIZE_MARKER = Symbol("anywidget.initialize");

/**
 * @param {import("@jupyter-widgets/base").DOMWidgetModel} model
 * @param {unknown} context
 * @return {import("@anywidget/types").AnyModel}
 *
 * Prunes the view down to the minimum context necessary.
 *
 * Calls to `model.get` and `model.set` automatically add the
 * `context`, so we can gracefully unsubscribe from events
 * added by user-defined hooks.
 */
function model_proxy(model, context) {
	return {
		get: model.get.bind(model),
		set: model.set.bind(model),
		save_changes: model.save_changes.bind(model),
		send: model.send.bind(model),
		// @ts-expect-error
		on(name, callback) {
			model.on(name, callback, context);
		},
		off(name, callback) {
			model.off(name, callback, context);
		},
		widget_manager: model.widget_manager,
	};
}

/**
 * @param {undefined | (() => Promise<void>)} fn
 * @param {string} kind
 */
async function safe_cleanup(fn, kind) {
	return Promise.resolve()
		.then(() => fn?.())
		.catch((e) => console.warn(`[anywidget] error cleaning up ${kind}.`, e));
}

class Runtime {
	/** @type {() => void} */
	#disposer = () => {};
	/** @type {Set<() => void>} */
	#view_disposers = new Set();
	/** @type {import('solid-js').Accessor<AnyWidget["render"] | null>} */
	#render = () => null;

	/** @param {import("@jupyter-widgets/base").DOMWidgetModel} model */
	constructor(model) {
		this.#disposer = createRoot((dispose) => {
			let [css, set_css] = createSignal(model.get("_css"));
			model.on("change:_css", () => {
				let id = model.get("_anywidget_id");
				console.debug(`[anywidget] css hot updated: ${id}`);
				set_css(model.get("_css"));
			});
			createEffect(() => {
				let id = model.get("_anywidget_id");
				load_css(css(), id);
			});

			/** @type {import("solid-js").Signal<string>} */
			let [esm, setEsm] = createSignal(model.get("_esm"));
			model.on("change:_esm", async () => {
				let id = model.get("_anywidget_id");
				console.debug(`[anywidget] esm hot updated: ${id}`);
				setEsm(model.get("_esm"));
			});

			let [render, set_render] = createSignal(
				/** @type {AnyWidget["render"] | null} */ (null),
			);
			this.#render = render;

			/** @type {Array<() => Promise<void>>} */
			let stack = [];
			createEffect(() => {
				// Make sure we track the signal in this effect.
				let new_esm = esm();
				// Cleanup the previous widget and load the new one.
				safe_cleanup(stack.pop(), "initialize")
					.then(async () => {
						// Load the new widget.
						let widget = await load_widget(new_esm);
						// Clear all previous event listeners from this hook.
						model.off(null, null, INITIALIZE_MARKER);
						// Run the initialize hook.
						let next = await widget.initialize?.({
							model: model_proxy(model, INITIALIZE_MARKER),
						});
						// Set the render signal, triggering render effects.
						set_render(() => widget.render);
						// Push the next cleanup onto the stack.
						stack.push(async () => next?.());
					});
			});
			return () => {
				stack.forEach((cleanup) => cleanup());
				stack.length = 0;
				model.off("change:_css");
				model.off("change:_esm");
				dispose();
			};
		});
	}

	/**
	 * @param {import("@jupyter-widgets/base").DOMWidgetView} view
	 * @returns {Promise<() => void>}
	 */
	async create_view(view) {
		let model = view.model;
		let disposer = createRoot((dispose) => {
			/** @type {Array<() => Promise<void>>} */
			let stack = [];

			// Register an effect for any time render changes.
			createEffect(() => {
				let render = this.#render();
				// Cleanup the previous render and load the new one.
				safe_cleanup(stack.pop(), "render")
					.then(async () => {
						// Clear all previous event listeners from this hook.
						model.off(null, null, view);
						view.$el.empty();
						// Run the render hook.
						let next = await render?.({
							model: model_proxy(model, view),
							el: view.el,
						});
						// Push the next cleanup onto the stack.
						stack.push(async () => next?.());
					});
			});
			return () => {
				dispose();
				stack.forEach((cleanup) => cleanup());
				stack.length = 0;
			};
		});
		// Have the runtime keep track but allow the view to dispose itself.
		this.#view_disposers.add(disposer);
		return () => {
			let deleted = this.#view_disposers.delete(disposer);
			if (deleted) disposer();
		};
	}

	dispose() {
		this.#view_disposers.forEach((dispose) => dispose());
		this.#view_disposers.clear();
		this.#disposer();
	}
}

/** @param {typeof import("@jupyter-widgets/base")} base */
export default function ({ DOMWidgetModel, DOMWidgetView }) {
	/** @type {WeakMap<AnyModel, Runtime>} */
	let RUNTIMES = new WeakMap();

	class AnyModel extends DOMWidgetModel {
		static model_name = "AnyModel";
		static model_module = name;
		static model_module_version = version;

		static view_name = "AnyView";
		static view_module = name;
		static view_module_version = version;

		/** @param {Parameters<InstanceType<DOMWidgetModel>["initialize"]>} args */
		initialize(...args) {
			super.initialize(...args);
			let runtime = new Runtime(this);
			this.once("destroy", () => {
				try {
					runtime.dispose();
				} finally {
					RUNTIMES.delete(this);
				}
			});
			RUNTIMES.set(this, runtime);
		}

		/**
		 * @param {Record<string, any>} state
		 *
		 * We override to support binary trailets because JSON.parse(JSON.stringify())
		 * does not properly clone binary data (it just returns an empty object).
		 *
		 * https://github.com/jupyter-widgets/ipywidgets/blob/47058a373d2c2b3acf101677b2745e14b76dd74b/packages/base/src/widget.ts#L562-L583
		 */
		serialize(state) {
			let serializers =
				/** @type {DOMWidgetModel} */ (this.constructor).serializers || {};
			for (let k of Object.keys(state)) {
				try {
					let serialize = serializers[k]?.serialize;
					if (serialize) {
						state[k] = serialize(state[k], this);
					} else if (k === "layout" || k === "style") {
						// These keys come from ipywidgets, rely on JSON.stringify trick.
						state[k] = JSON.parse(JSON.stringify(state[k]));
					} else {
						state[k] = structuredClone(state[k]);
					}
					if (typeof state[k]?.toJSON === "function") {
						state[k] = state[k].toJSON();
					}
				} catch (e) {
					console.error("Error serializing widget state attribute: ", k);
					throw e;
				}
			}
			return state;
		}
	}

	class AnyView extends DOMWidgetView {
		/** @type {undefined | (() => void)} */
		#dispose = undefined;
		async render() {
			let runtime = RUNTIMES.get(this.model);
			assert(runtime, "[anywidget] runtime not found.");
			assert(!this.#dispose, "[anywidget] dispose already set.");
			this.#dispose = await runtime.create_view(this);
		}
		remove() {
			this.#dispose?.();
			super.remove();
		}
	}

	return { AnyModel, AnyView };
}
