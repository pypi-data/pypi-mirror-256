"use strict";
(self["webpackChunkjupyterlab_kishu"] = self["webpackChunkjupyterlab_kishu"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestAPI: () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'kishu', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    const data = await response.text();
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data);
    }
    if (data.length > 0) {
        try {
            return JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data);
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");





const PLUGIN_ID = 'jupyterlab_kishu:plugin';
var CommandIDs;
(function (CommandIDs) {
    /**
     * Initialize Kishu on the currently viewed notebook.
     */
    CommandIDs.init = 'kishu:init';
    /**
     * Checkout a commit on the currently viewed notebook.
     */
    CommandIDs.checkout = 'kishu:checkout';
    /**
     * Create a commit on the currently viewed notebook.
     */
    CommandIDs.commit = 'kishu:commit';
})(CommandIDs || (CommandIDs = {}));
var KishuSetting;
(function (KishuSetting) {
    KishuSetting.kishu_dir = "";
})(KishuSetting || (KishuSetting = {}));
function notifyError(message) {
    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Notification.error(message, { autoClose: 3000 });
}
function currentNotebookPath(tracker) {
    const widget = tracker.currentWidget;
    if (!widget) {
        console.log(`Missing tracker widget to detect currently viewed notebook.`);
        return undefined;
    }
    return widget.context.localPath;
}
function commitSummaryToString(commit) {
    const date = new Date(commit.timestamp);
    return `[${date.toLocaleString()}]: ${commit.message} (${commit.commit_id})`;
}
function extractHashFromString(inputString) {
    const regex = /\(([0-9a-fA-F-]+)\)$/;
    const match = inputString.match(regex);
    if (match && match[1]) {
        return match[1];
    }
    return undefined;
}
function loadSetting(setting) {
    // Read the settings and convert to the correct type
    KishuSetting.kishu_dir = setting.get('kishu_dir').composite;
    console.log(`Settings: kishu_dir= ${KishuSetting.kishu_dir}`);
}
function installCommands(app, palette, translator, tracker) {
    const { commands } = app;
    const trans = translator.load('jupyterlab');
    /**
     * Init
     */
    commands.addCommand(CommandIDs.init, {
        label: (args) => (args.label && args.label == 'short'
            ? trans.__('Initialize/Re-attach')
            : trans.__('Kishu: Initialize/Re-attach...')),
        execute: async (_args) => {
            // Detect currently viewed notebook.
            const notebook_path = currentNotebookPath(tracker);
            if (!notebook_path) {
                notifyError(trans.__(`No currently viewed notebook detected to initialize/attach.`));
                return;
            }
            // Make init request
            const init_promise = (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('init', {
                method: 'POST',
                body: JSON.stringify({ notebook_path: notebook_path }),
            });
            // Report.
            const notify_manager = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Notification.manager;
            const notify_id = notify_manager.notify(trans.__(`Initializing Kishu on ${notebook_path}...`), 'in-progress', { autoClose: false });
            init_promise.then((init_result) => {
                if (init_result.status != "ok") {
                    notify_manager.update({
                        id: notify_id,
                        message: trans.__(`Kishu init failed.\n"${init_result.message}"`),
                        type: 'error',
                        autoClose: 3000,
                    });
                }
                else {
                    notify_manager.update({
                        id: notify_id,
                        message: trans.__(`Kishu init succeeded!\n"${init_result.message}"`),
                        type: 'success',
                        autoClose: 3000,
                    });
                }
            });
        }
    });
    palette.addItem({
        command: CommandIDs.init,
        category: 'Kishu',
    });
    /**
     * Checkout
     */
    commands.addCommand(CommandIDs.checkout, {
        label: (args) => (args.label && args.label == 'short'
            ? trans.__('Checkout')
            : trans.__('Kishu: Checkout...')),
        execute: async (_args) => {
            var _a, _b;
            // Detect currently viewed notebook.
            const notebook_path = currentNotebookPath(tracker);
            if (!notebook_path) {
                notifyError(trans.__(`No currently viewed notebook detected to checkout.`));
                return;
            }
            // List all commits.
            const log_all_result = await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('log_all', {
                method: 'POST',
                body: JSON.stringify({ notebook_path: notebook_path }),
            });
            // Ask for the target commit ID.
            let maybe_commit_id = undefined;
            if (!log_all_result || log_all_result.commit_graph.length == 0) {
                // Failed to list, asking in text dialog directly.
                maybe_commit_id = (_a = (await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.InputDialog.getText({
                    placeholder: '<commit_id>',
                    title: trans.__('Checkout to...'),
                    okLabel: trans.__('Checkout')
                })).value) !== null && _a !== void 0 ? _a : undefined;
                if (!maybe_commit_id) {
                    notifyError(trans.__(`Kishu checkout requires commit ID.`));
                }
            }
            else {
                // Find the index to current commit.
                let current_idx = log_all_result.commit_graph.findIndex(commit => commit.commit_id === log_all_result.head.commit_id);
                if (current_idx == -1) {
                    current_idx = log_all_result.commit_graph.length - 1;
                }
                // Show the list and ask to pick one item
                const selected_commit_str = (_b = (await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.InputDialog.getItem({
                    items: log_all_result.commit_graph.map(commitSummaryToString),
                    current: current_idx,
                    editable: false,
                    title: trans.__('Checkout to...'),
                    okLabel: trans.__('Checkout')
                })).value) !== null && _b !== void 0 ? _b : undefined;
                if (selected_commit_str !== undefined) {
                    maybe_commit_id = extractHashFromString(selected_commit_str);
                }
            }
            if (!maybe_commit_id) {
                return;
            }
            const commit_id = maybe_commit_id;
            // Make checkout request
            const checkout_promise = (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('checkout', {
                method: 'POST',
                body: JSON.stringify({ notebook_path: notebook_path, commit_id: commit_id }),
            });
            // Reports.
            const notify_manager = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Notification.manager;
            const notify_id = notify_manager.notify(trans.__(`Checking out ${commit_id}...`), 'in-progress', { autoClose: false });
            checkout_promise.then((checkout_result) => {
                if (checkout_result.status != "ok") {
                    notify_manager.update({
                        id: notify_id,
                        message: trans.__(`Kishu checkout failed.\n"${checkout_result.message}"`),
                        type: 'error',
                        autoClose: 3000,
                    });
                }
                else {
                    notify_manager.update({
                        id: notify_id,
                        message: trans.__(`Kishu checkout to ${commit_id} succeeded!`),
                        type: 'success',
                        autoClose: 3000,
                    });
                }
            });
        }
    });
    palette.addItem({
        command: CommandIDs.checkout,
        category: 'Kishu',
    });
    /**
     * Commit
     */
    commands.addCommand(CommandIDs.commit, {
        label: (args) => (args.label && args.label == 'short'
            ? trans.__('Commit')
            : trans.__('Kishu: Commit...')),
        execute: async (_args) => {
            var _a;
            // Detect currently viewed notebook.
            const notebook_path = currentNotebookPath(tracker);
            if (!notebook_path) {
                notifyError(trans.__(`No currently viewed notebook detected to ommit.`));
                return;
            }
            // Ask for the commit message.
            const message = (_a = (await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.InputDialog.getText({
                placeholder: '<commit_message>',
                title: trans.__('Commit message'),
                okLabel: trans.__('Commit')
            })).value) !== null && _a !== void 0 ? _a : undefined;
            if (message == undefined) {
                notifyError(trans.__(`Kishu commit requires a commit message.`));
            }
            if (!message) {
                return;
            }
            // Make checkout request
            const commit_promise = (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('commit', {
                method: 'POST',
                body: JSON.stringify({ notebook_path: notebook_path, message: message }),
            });
            // Reports.
            const notify_manager = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Notification.manager;
            const notify_id = notify_manager.notify(trans.__(`Creating a commit...`), 'in-progress', { autoClose: false });
            commit_promise.then((commit_result) => {
                if (commit_result.status != "ok") {
                    notify_manager.update({
                        id: notify_id,
                        message: trans.__(`Kishu commit failed.\n"${commit_result.message}"`),
                        type: 'error',
                        autoClose: 3000,
                    });
                }
                else {
                    notify_manager.update({
                        id: notify_id,
                        message: trans.__(`Kishu commit succeeded!`),
                        type: 'success',
                        autoClose: 3000,
                    });
                }
            });
        }
    });
    palette.addItem({
        command: CommandIDs.commit,
        category: 'Kishu',
    });
}
/**
 * Initialization data for the jupyterlab_kishu extension.
 */
const plugin = {
    id: PLUGIN_ID,
    description: 'Jupyter extension to interact with Kishu',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker],
    activate: (app, palette, translator, settings, tracker) => {
        Promise.all([app.restored, settings.load(PLUGIN_ID)])
            .then(([, setting]) => {
            // Setting registry.
            loadSetting(setting);
            setting.changed.connect(loadSetting);
            // Install commands.
            installCommands(app, palette, translator, tracker);
        })
            .catch(reason => {
            console.error(`Something went wrong when reading the settings.\n${reason}`);
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.52a20810e9eaf8c7bf29.js.map