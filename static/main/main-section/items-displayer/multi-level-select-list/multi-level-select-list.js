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
    // static ItemData = class {
    //     names: Array<string>
    // }
    MyApi.Names = /** @class */ (function () {
        function class_1() {
        }
        return class_1;
    }());
    MyApi.Get = /** @class */ (function () {
        function class_2() {
        }
        class_2.storagesNames = function () {
            return Api.get("api/storages_names")
                .then(function (object) { return object.names; });
        };
        class_2.containerNames = function (storageName) {
            return Api.get("api/storage/".concat(storageName, "/containers_names"))
                .then(function (object) { return object.names; });
        };
        class_2.itemNames = function (storageName, containerName) {
            var path = "api/storage/".concat(storageName, "/container/").concat(containerName, "/items_names");
            return Api.get(path)
                .then(function (object) { return object.names; });
        };
        return class_2;
    }());
    return MyApi;
}());
MyApi.Get.containerNames("TestStorageName").then(function (storages) {
    console.log(storages);
});
MyApi.Get.itemNames("TestStorageName", "TestContainerName").then(function (storages) {
    console.log(storages);
});
// MyApi.Get.item("TestStorageName", "TestContainerName").then(storages => {
//     console.log(storages)
// })
var MultiLevelSelectListManager = /** @class */ (function () {
    function MultiLevelSelectListManager() {
    }
    // In case null in selectedOption - select first one.
    MultiLevelSelectListManager.createSelectElementCode = function (name, options, selectedOption, onChange) {
        if (selectedOption === void 0) { selectedOption = null; }
        var opening = "<label for=\"".concat(name, "\"></label>\n") +
            "<select id=\"".concat(name, "\" name=\"").concat(name, "\" ") +
            "class=\"my-selector\" onchange=\"".concat(onChange, "\">");
        var options_ = options.map(function (option) {
            if (selectedOption == option)
                return "  <option value=\"".concat(option, "\" selected>").concat(option.toUpperCase(), "</option>");
            else
                return "  <option value=\"".concat(option, "\">").concat(option.toUpperCase(), "</option>");
        });
        var closing = '</select>';
        return opening + "\n" + options_.join("\n") + "\n" + closing + "\n";
    };
    // Overwrite storages section in HTMl.
    MultiLevelSelectListManager.updateStorages = function (storages) {
        if (MultiLevelSelectListManager.storageSelectedOption == null)
            MultiLevelSelectListManager.storageSelectedOption = storages[0];
        var selectElementCode = MultiLevelSelectListManager.createSelectElementCode("my-selector-storage", storages, MultiLevelSelectListManager.storageSelectedOption, "MultiLevelSelectListManager.update(value, null)");
        var header = document.getElementsByClassName("multi-level-select-list")[0];
        header.insertAdjacentHTML("beforeend", selectElementCode);
    };
    // Overwrite containers section in HTMl.
    MultiLevelSelectListManager.updateContainers = function (containers) {
        if (MultiLevelSelectListManager.containerSelectedOption == null)
            MultiLevelSelectListManager.containerSelectedOption = containers[0];
        var selectElementCode = MultiLevelSelectListManager.createSelectElementCode("my-selector-container", containers, MultiLevelSelectListManager.containerSelectedOption, "MultiLevelSelectListManager.update(null, value)");
        var header = document.getElementsByClassName("multi-level-select-list")[0];
        header.insertAdjacentHTML("beforeend", selectElementCode);
    };
    MultiLevelSelectListManager.update = function (storageNewOption, containerNewOption) {
        if (storageNewOption === void 0) { storageNewOption = null; }
        if (containerNewOption === void 0) { containerNewOption = null; }
        var callWhenStorageDataArrive = function (storageNames) {
            // Update storage value to received one (it may be null).
            if (storageNewOption != null)
                MultiLevelSelectListManager.storageSelectedOption = storageNewOption;
            // Update container value to received one (it may be null).
            MultiLevelSelectListManager.containerSelectedOption = containerNewOption;
            // Update storage list - HTML, cached values.
            MultiLevelSelectListManager.updateStorages(storageNames);
        };
        var callWhenContainerDataArrive = function (containerNames) {
            // Update storage value to received one (it may be null).
            MultiLevelSelectListManager.containerSelectedOption = containerNewOption;
            // Update container list - HTML, cached values.
            MultiLevelSelectListManager.updateContainers(containerNames);
        };
        // Receive all storages from server to ensure chosen one still exists.
        MyApi.Get.storagesNames()
            .then(function (storageNames) {
            var selectHeader = document.getElementsByClassName("multi-level-select-list")[0];
            selectHeader.replaceChildren();
            callWhenStorageDataArrive(storageNames);
            MyApi.Get.containerNames(MultiLevelSelectListManager.storageSelectedOption)
                .then(function (containerNames) {
                callWhenContainerDataArrive(containerNames);
            });
        });
    };
    MultiLevelSelectListManager.storageSelectedOption = null;
    MultiLevelSelectListManager.containerSelectedOption = null;
    return MultiLevelSelectListManager;
}());
