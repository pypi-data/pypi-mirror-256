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
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");




var CommandIDs;
(function (CommandIDs) {
    /**
     * Checkout a commit on the currently viewed file.
     */
    CommandIDs.checkout = 'kishu:checkout';
})(CommandIDs || (CommandIDs = {}));
function commitSummaryToString(commit) {
    return `[${commit.commit_id}] ${commit.message}`;
}
function extractHashFromString(inputString) {
    const regex = /\[([a-fA-F0-9-]+)\]\s/;
    const match = inputString.match(regex);
    if (match && match[1]) {
        return match[1];
    }
    return undefined;
}
/**
 * Initialization data for the jupyterlab_kishu extension.
 */
const plugin = {
    id: 'jupyterlab_kishu:plugin',
    description: 'Jupyter extension to interact with Kishu',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.ITranslator],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry],
    activate: (app, palette, translator, settingRegistry) => {
        const { commands } = app;
        const trans = translator.load('jupyterlab');
        if (settingRegistry) {
            settingRegistry
                .load(plugin.id)
                .then(settings => {
                console.log('jupyterlab_kishu settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.error('Failed to load settings for jupyterlab_kishu.', reason);
            });
        }
        /**
         * Checkout
         */
        commands.addCommand(CommandIDs.checkout, {
            label: trans.__('Kishu: Checkout...'),
            execute: async (_args) => {
                var _a, _b, _c;
                // TODO: Detect currently viewed notebook path.
                const notebook_id = (_a = (await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.InputDialog.getText({
                    placeholder: '<notebook_id>',
                    title: trans.__('Checkout...'),
                    okLabel: trans.__('Next')
                })).value) !== null && _a !== void 0 ? _a : undefined;
                if (!notebook_id) {
                    window.alert(trans.__(`Kishu checkout requires notebook ID.`));
                    return;
                }
                // List all commits.
                const log_all_result = await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('log_all', {
                    method: 'POST',
                    body: JSON.stringify({ notebook_id: notebook_id }),
                });
                // Ask for the target commit ID.
                let commit_id = undefined;
                if (!log_all_result || log_all_result.commit_graph.length == 0) {
                    // Failed to list, asking in text dialog directly.
                    commit_id = (_b = (await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.InputDialog.getText({
                        placeholder: '<commit_id>',
                        title: trans.__('Checkout to...'),
                        okLabel: trans.__('Checkout')
                    })).value) !== null && _b !== void 0 ? _b : undefined;
                }
                else {
                    // Show the list and ask to pick one item
                    const selected_commit_str = (_c = (await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.InputDialog.getItem({
                        items: log_all_result.commit_graph.map(commitSummaryToString),
                        current: log_all_result.commit_graph.length - 1,
                        editable: false,
                        title: trans.__('Checkout to...'),
                        okLabel: trans.__('Checkout')
                    })).value) !== null && _c !== void 0 ? _c : undefined;
                    if (selected_commit_str !== undefined) {
                        console.log(`Selected selected_commit_str= ${selected_commit_str}`);
                        commit_id = extractHashFromString(selected_commit_str);
                    }
                }
                if (!commit_id) {
                    window.alert(trans.__(`Kishu checkout requires commit ID.`));
                    return;
                }
                console.log(`Selected commit_id= ${commit_id}`);
                // Make checkout request
                const checkout_result = await (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('checkout', {
                    method: 'POST',
                    body: JSON.stringify({ notebook_id: notebook_id, commit_id: commit_id }),
                });
                // Report.
                if (checkout_result.status != 'ok') {
                    window.alert(trans.__(`Kishu checkout failed: "${checkout_result.message}"`));
                }
                else {
                    window.alert(trans.__(`Kishu checkout to ${commit_id} succeeded.\nPlease refresh this page.`));
                }
            }
        });
        palette.addItem({
            command: CommandIDs.checkout,
            category: 'Kishu',
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.3957db087d97ee6ddfd2.js.map