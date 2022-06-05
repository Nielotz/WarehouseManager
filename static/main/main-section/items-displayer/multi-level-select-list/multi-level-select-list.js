var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var Api = /** @class */ (function () {
    function Api() {
    }
    Api.get = function (url) {
        return fetch(url)
            .then(function (response) {
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            return response.json();
        });
    };
    return Api;
}());
var MyApi = /** @class */ (function () {
    function MyApi() {
    }
    MyApi.Thing = /** @class */ (function () {
        function class_1() {
        }
        return class_1;
    }());
    MyApi.Storage = /** @class */ (function (_super) {
        __extends(class_2, _super);
        function class_2() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        return class_2;
    }(MyApi.Thing));
    MyApi.Container = /** @class */ (function (_super) {
        __extends(class_3, _super);
        function class_3() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        return class_3;
    }(MyApi.Thing));
    MyApi.Get = /** @class */ (function () {
        function class_4() {
        }
        class_4.storages = function () {
            return MyApi.Get.ask_for("api/storages");
        };
        class_4.containers = function (storageId) {
            return MyApi.Get.ask_for("api/storages/".concat(storageId, "/containers"));
        };
        class_4.items = function (storageId, containerId) {
            return MyApi.Get.ask_for("api/storages/".concat(storageId, "/containers/").concat(containerId, "/items"));
        };
        class_4.ask_for = function (path) {
            return Api.get(path);
        };
        return class_4;
    }());
    return MyApi;
}());
var MultiLevelSelectListManager = /** @class */ (function () {
    function MultiLevelSelectListManager() {
    }
    // In case null in selectedOption - select first one.
    MultiLevelSelectListManager.generateSelectElementHtml = function (htmlElementIdName, selected, optionsIdName, onChange) {
        var openingHtml = "<label for=\"".concat(htmlElementIdName, "\"></label>\n") +
            "<select id=\"".concat(htmlElementIdName, "\" name=\"").concat(htmlElementIdName, "\" ") +
            "class=\"my-selector\" onchange=\"".concat(onChange, "\">");
        var optionsHtml = optionsIdName.map(function (option) {
            if (selected !== null && selected.id === option.id)
                return "  <option value=".concat(option.id, " selected>").concat(option.name.toUpperCase(), "</option>");
            else
                return "  <option value=".concat(option.id, ">").concat(option.name.toUpperCase(), "</option>");
        });
        var closingHtml = '</select>';
        return openingHtml + "\n" + optionsHtml.join("\n") + "\n" + closingHtml + "\n";
    };
    // Overwrite storages section in HTMl.
    MultiLevelSelectListManager.updateStorages = function (storages, selected) {
        if (selected === void 0) { selected = null; }
        if (selected === null && storages.length)
            selected = storages[0];
        var selectElementCode = MultiLevelSelectListManager.generateSelectElementHtml("my-selector-storage", selected, storages, "MultiLevelSelectListManager.update(value, null)");
        var header = document.getElementsByClassName("multi-level-select-list")[0];
        header.insertAdjacentHTML("beforeend", selectElementCode);
    };
    // Overwrite containers section in HTMl.
    MultiLevelSelectListManager.updateContainers = function (containers, selected) {
        if (selected === void 0) { selected = null; }
        if (selected === null && containers.length)
            selected = containers[0];
        var selectElementCode = MultiLevelSelectListManager.generateSelectElementHtml("my-selector-container", selected, containers, "MultiLevelSelectListManager.update(this.parentElement.querySelector('#my-selector-storage').value, value)");
        var header = document.getElementsByClassName("multi-level-select-list")[0];
        header.insertAdjacentHTML("beforeend", selectElementCode);
    };
    // Update MultiLevelSelectList (modifies HTML).
    MultiLevelSelectListManager.update = function (selectedStorageId, selectedContainerId) {
        if (selectedStorageId === void 0) { selectedStorageId = null; }
        if (selectedContainerId === void 0) { selectedContainerId = null; }
        if (selectedStorageId !== null)
            selectedStorageId = Number(selectedStorageId);
        if (selectedContainerId !== null)
            selectedContainerId = Number(selectedContainerId);
        var callWhenStorageDataArrive = function (storages) {
            var selectedStorage = null;
            if (selectedStorageId !== null) {
                var selectedStorage_ = storages.filter(function (storage) { return storage.id === selectedStorageId; });
                if (selectedStorage_.length) {
                    selectedStorage = selectedStorage_[0];
                }
                else {
                    // TODO: Error handling: selected option does not exists in database.
                    alert("Selected storage_id(".concat(selectedStorageId, ") does not exists in db."));
                }
            }
            else if (storages.length) {
                selectedStorage = storages[0];
            }
            // Update storage list - HTML, cached values.
            MultiLevelSelectListManager.updateStorages(storages, selectedStorage);
            return selectedStorage;
        };
        var callWhenContainerDataArrive = function (containers) {
            // Update container list - HTML, cached values.
            var selectedContainer = null;
            if (selectedContainerId !== null) {
                var selectedContainer_ = containers.filter(function (container) { return container.id === selectedContainerId; });
                if (selectedContainer_.length) {
                    selectedContainer = selectedContainer_[0];
                }
                else {
                    // TODO: Error handling: selected option does not exists in database.
                    alert("Selected container_id(".concat(selectedContainerId, ") does not exists in db."));
                }
            }
            else if (containers.length) {
                selectedContainer = containers[0];
            }
            MultiLevelSelectListManager.updateContainers(containers, selectedContainer);
        };
        // Receive all storages from server to ensure chosen one still exists.
        MyApi.Get.storages()
            .then(function (storages) {
            var selectHeader = document.getElementsByClassName("multi-level-select-list")[0];
            selectHeader.replaceChildren();
            var selectedStorage = callWhenStorageDataArrive(storages);
            MyApi.Get.containers(selectedStorage.id)
                .then(function (containers) {
                callWhenContainerDataArrive(containers);
            });
        });
    };
    return MultiLevelSelectListManager;
}());
