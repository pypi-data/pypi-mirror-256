"use strict";
(self["webpackChunkastronbs"] = self["webpackChunkastronbs"] || []).push([["lib_index_js"],{

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
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'astronbs', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
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
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");






/**
 * Initialization data for the astronbs extension.
 */
const plugin = {
    id: 'astronbs:plugin',
    autoStart: true,
    optional: [
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry,
        _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.ILauncher,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.IFileBrowserFactory,
        _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2__.IDocumentManager
    ],
    activate: (app, settingRegistry, launcher, fileBrowser, docManager) => {
        console.log('JupyterLab extension astronbs is activated!');
        if (settingRegistry) {
            settingRegistry
                .load(plugin.id)
                .then(settings => {
                console.log('astronbs settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.error('Failed to load settings for astronbs.', reason);
            });
        }
        app.commands.addCommand('astronbs:reduction_template', {
            // code to run when this command is executed
            execute: () => {
                const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('reduction_template', {
                    body: JSON.stringify({
                        path: fileBrowser.defaultBrowser.model.path,
                        package_path: 'astronbs.notebooks',
                        nb_name: 'reduction_template.ipynb'
                    }),
                    method: 'POST'
                });
                console.log(reply);
                reply.then(data => {
                    console.log(data);
                    if (docManager) {
                        docManager.open(data['path']);
                    }
                });
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.imageIcon,
            label: 'Reduction Template'
        });
        app.commands.addCommand('astronbs:reprojection_template', {
            // code to run when this command is executed
            execute: () => {
                const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('reprojection_template', {
                    body: JSON.stringify({ path: fileBrowser.defaultBrowser.model.path }),
                    method: 'POST'
                });
                console.log(reply);
                reply.then(data => {
                    console.log(data);
                    if (docManager) {
                        docManager.open(data['path']);
                    }
                });
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.imageIcon,
            label: 'Reprojection Template'
        });
        app.commands.addCommand('astronbs:light_combo_template', {
            // code to run when this command is executed
            execute: () => {
                const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('light_combo_template', {
                    body: JSON.stringify({ path: fileBrowser.defaultBrowser.model.path }),
                    method: 'POST'
                });
                console.log('I am back in open2');
                console.log(reply);
                reply.then(data => {
                    console.log(data);
                    if (docManager) {
                        docManager.open(data['path']);
                    }
                });
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.imageIcon,
            label: 'Light Combo Template'
        });
        app.commands.addCommand('astronbs:folder_viewer_template', {
            // code to run when this command is executed
            execute: () => {
                const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('folder_viewer_template', {
                    body: JSON.stringify({ path: fileBrowser.defaultBrowser.model.path }),
                    method: 'POST'
                });
                console.log('I am back in open15');
                console.log(reply);
                reply.then(data => {
                    console.log(data);
                    if (docManager) {
                        docManager.open(data['path']);
                    }
                });
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.imageIcon,
            label: 'Folder Image Viewer'
        });
        app.commands.addCommand('astronbs:interactive_image_viewer', {
            // code to run when this command is executed
            execute: () => {
                const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('interactive_image_viewer', {
                    body: JSON.stringify({ path: fileBrowser.defaultBrowser.model.path }),
                    method: 'POST'
                });
                console.log('I am back in open11');
                console.log(reply);
                reply.then(data => {
                    console.log(data);
                    if (docManager) {
                        docManager.open(data['path']);
                    }
                });
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.imageIcon,
            label: 'Interactive Image Viewer'
        });
        app.commands.addCommand('astronbs:quick_color_template', {
            // code to run when this command is executed
            execute: () => {
                const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('quick_color_template', {
                    body: JSON.stringify({ path: fileBrowser.defaultBrowser.model.path }),
                    method: 'POST'
                });
                console.log('I am back in open11');
                console.log(reply);
                reply.then(data => {
                    console.log(data);
                    if (docManager) {
                        docManager.open(data['path']);
                    }
                });
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.imageIcon,
            label: 'Quick Color Image'
        });
        app.commands.addCommand('astronbs:color_mixer_template', {
            // code to run when this command is executed
            execute: () => {
                const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('color_mixer_template', {
                    body: JSON.stringify({ path: fileBrowser.defaultBrowser.model.path }),
                    method: 'POST'
                });
                console.log('I am back in open11');
                console.log(reply);
                reply.then(data => {
                    console.log(data);
                    if (docManager) {
                        docManager.open(data['path']);
                    }
                });
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.imageIcon,
            label: 'Color Mixer'
        });
        app.commands.addCommand('astronbs:01_seeing_profile', {
            // code to run when this command is executed
            execute: () => {
                const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('nb_make', {
                    body: JSON.stringify({
                        path: fileBrowser.defaultBrowser.model.path,
                        package_path: 'stellarphot.notebooks.photometry',
                        nb_name: '01-viewer-seeing-template.ipynb'
                    }),
                    method: 'POST'
                });
                console.log(reply);
                reply.then(data => {
                    console.log(data);
                    if (docManager) {
                        docManager.open(data['path']);
                    }
                });
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.imageIcon,
            label: '01 Seeing Profile'
        });
        app.commands.addCommand('astronbs:02_comp_stars', {
            // code to run when this command is executed
            execute: () => {
                const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('nb_make', {
                    body: JSON.stringify({
                        path: fileBrowser.defaultBrowser.model.path,
                        package_path: 'stellarphot.notebooks.photometry',
                        nb_name: '02-comp-star-plotter-template.ipynb'
                    }),
                    method: 'POST'
                });
                console.log(reply);
                reply.then(data => {
                    console.log(data);
                    if (docManager) {
                        docManager.open(data['path']);
                    }
                });
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.imageIcon,
            label: '02 Comparison Stars'
        });
        app.commands.addCommand('astronbs:03_do_photometry', {
            // code to run when this command is executed
            execute: () => {
                const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('nb_make', {
                    body: JSON.stringify({
                        path: fileBrowser.defaultBrowser.model.path,
                        package_path: 'stellarphot.notebooks.photometry',
                        nb_name: '03-photometry-template.ipynb'
                    }),
                    method: 'POST'
                });
                console.log(reply);
                reply.then(data => {
                    console.log(data);
                    if (docManager) {
                        docManager.open(data['path']);
                    }
                });
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.imageIcon,
            label: '03 Do photometry'
        });
        app.commands.addCommand('astronbs:04_transform_pared_back', {
            // code to run when this command is executed
            execute: () => {
                const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('nb_make', {
                    body: JSON.stringify({
                        path: fileBrowser.defaultBrowser.model.path,
                        package_path: 'stellarphot.notebooks.photometry',
                        nb_name: '04-transform-pared-back.ipynb'
                    }),
                    method: 'POST'
                });
                console.log(reply);
                reply.then(data => {
                    console.log(data);
                    if (docManager) {
                        docManager.open(data['path']);
                    }
                });
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.imageIcon,
            label: '04 Transform photometry'
        });
        app.commands.addCommand('astronbs:05_relative_flux', {
            // code to run when this command is executed
            execute: () => {
                const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('nb_make', {
                    body: JSON.stringify({
                        path: fileBrowser.defaultBrowser.model.path,
                        package_path: 'stellarphot.notebooks.photometry',
                        nb_name: '05-relative-flux-calculation-template.ipynb'
                    }),
                    method: 'POST'
                });
                console.log(reply);
                reply.then(data => {
                    console.log(data);
                    if (docManager) {
                        docManager.open(data['path']);
                    }
                });
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.imageIcon,
            label: '05 Relative flux'
        });
        app.commands.addCommand('astronbs:06_transit_fitting', {
            // code to run when this command is executed
            execute: () => {
                const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('nb_make', {
                    body: JSON.stringify({
                        path: fileBrowser.defaultBrowser.model.path,
                        package_path: 'stellarphot.notebooks.photometry',
                        nb_name: '06-transit-fit-template.ipynb'
                    }),
                    method: 'POST'
                });
                console.log(reply);
                reply.then(data => {
                    console.log(data);
                    if (docManager) {
                        docManager.open(data['path']);
                    }
                });
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.imageIcon,
            label: '06 Transit fitting'
        });
        app.commands.addCommand('astronbs:07_transit_fitting_exotic', {
            // code to run when this command is executed
            execute: () => {
                const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('nb_make', {
                    body: JSON.stringify({
                        path: fileBrowser.defaultBrowser.model.path,
                        package_path: 'stellarphot.notebooks.photometry',
                        nb_name: '07-transit-fit-with-exotic.ipynb'
                    }),
                    method: 'POST'
                });
                console.log(reply);
                reply.then(data => {
                    console.log(data);
                    if (docManager) {
                        docManager.open(data['path']);
                    }
                });
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.imageIcon,
            label: '07 Transit fitting EXOTIC'
        });
        // Add item to launcher
        if (launcher) {
            launcher.add({
                command: 'astronbs:reduction_template',
                category: 'Astro',
                rank: 0
            });
            launcher.add({
                command: 'astronbs:reprojection_template',
                category: 'Astro',
                rank: 10
            });
            launcher.add({
                command: 'astronbs:light_combo_template',
                category: 'Astro',
                rank: 20
            });
            launcher.add({
                command: 'astronbs:folder_viewer_template',
                category: 'Astro',
                rank: 30
            });
            launcher.add({
                command: 'astronbs:interactive_image_viewer',
                category: 'Astro',
                rank: 40
            });
            launcher.add({
                command: 'astronbs:quick_color_template',
                category: 'Astro',
                rank: 50
            });
            launcher.add({
                command: 'astronbs:color_mixer_template',
                category: 'Astro',
                rank: 60
            });
            launcher.add({
                command: 'astronbs:01_seeing_profile',
                category: 'Photometry',
                rank: 0
            });
            launcher.add({
                command: 'astronbs:02_comp_stars',
                category: 'Photometry',
                rank: 0
            });
            launcher.add({
                command: 'astronbs:03_do_photometry',
                category: 'Photometry',
                rank: 0
            });
            launcher.add({
                command: 'astronbs:04_transform_pared_back',
                category: 'Photometry',
                rank: 0
            });
            launcher.add({
                command: 'astronbs:05_relative_flux',
                category: 'Photometry',
                rank: 0
            });
            launcher.add({
                command: 'astronbs:06_transit_fitting',
                category: 'Photometry',
                rank: 0
            });
            launcher.add({
                command: 'astronbs:07_transit_fitting_exotic',
                category: 'Photometry',
                rank: 0
            });
        }
        (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('get_example')
            .then(data => {
            console.log(data);
        })
            .catch(reason => {
            console.error(`The astronbs server extension appears to be missing.\n${reason}`);
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.9c75156769b24082bfee.js.map