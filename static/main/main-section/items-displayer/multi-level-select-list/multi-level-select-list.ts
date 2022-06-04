class Api {
    static get<T>(url: string): Promise<T> {
        return fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(response.statusText)
                }
                return response.json() as Promise<T>
            })
    }
}

class MyApi {
    static Names = class {
        names: Array<string>
    }

    static Get = class {
        static Names = class {
            static storages() {
                return MyApi.Get.Names.getNames("api/storages_names")
            }

            static containers(storageName: string) {
                return MyApi.Get.Names.getNames(`api/storage/${storageName}/containers_names`)
            }

            static items(storageName: string, containerName: string) {
                return MyApi.Get.Names.getNames(`api/storage/${storageName}/container/${containerName}/items_names`)
            }

            private static getNames(path: string) {
                return Api.get<InstanceType<typeof MyApi.Names>>(path).then(object => object.names)
            }
        }

        // static item(itemID: number) {
        //     let path: string = `api/item/${itemID}`
        //     return Api.get<InstanceType<typeof MyApi.ItemData>>(path)
        //         .then(object => object.names)
        // }

    }
}

MyApi.Get.Names.storages().then(storages => {
    console.log(storages)
})

MyApi.Get.Names.containers("TestStorageName").then(containers => {
    console.log(containers)
})

MyApi.Get.Names.items("TestStorageName", "TestContainerName").then(items => {
    console.log(items)
})

// MyApi.Get.item("TestStorageName", "TestContainerName").then(storages => {
//     console.log(storages)
// })

class MultiLevelSelectListManager {
    private static storageSelectedOption: string = null
    private static containerSelectedOption: string = null

    // In case null in selectedOption - select first one.
    private static createSelectElementCode(name: string, options: Array<string>,
                                           selectedOption: string = null, onChange: string) {
        let opening = `<label for="${name}"></label>\n` +
            `<select id="${name}" name="${name}" ` +
            `class="my-selector" onchange="${onChange}">`

        let options_ = options.map(option => {
            if (selectedOption == option)
                return `  <option value="${option}" selected>${option.toUpperCase()}</option>`
            else
                return `  <option value="${option}">${option.toUpperCase()}</option>`
        })
        let closing = '</select>'

        return opening + "\n" + options_.join("\n") + "\n" + closing + "\n"
    }

    // Overwrite storages section in HTMl.
    private static updateStorages(storages: Array<string>) {
        if (MultiLevelSelectListManager.storageSelectedOption == null && storages.length)
            MultiLevelSelectListManager.storageSelectedOption = storages[0]
        let selectElementCode: string =
            MultiLevelSelectListManager.createSelectElementCode("my-selector-storage",
                storages,
                MultiLevelSelectListManager.storageSelectedOption,
                "MultiLevelSelectListManager.update(value, null)")
        let header = document.getElementsByClassName("multi-level-select-list")[0]
        header.insertAdjacentHTML("beforeend", selectElementCode)
    }

    // Overwrite containers section in HTMl.
    private static updateContainers(containers: Array<string>) {
        if (MultiLevelSelectListManager.containerSelectedOption == null && containers.length)
            MultiLevelSelectListManager.containerSelectedOption = containers[0]
        let selectElementCode: string =
            MultiLevelSelectListManager.createSelectElementCode("my-selector-container",
                containers,
                MultiLevelSelectListManager.containerSelectedOption,
                "MultiLevelSelectListManager.update(null, value)")
        let header = document.getElementsByClassName("multi-level-select-list")[0]
        header.insertAdjacentHTML("beforeend", selectElementCode)
    }

    static update(storageNewOption: string = null, containerNewOption: string = null) {
        let callWhenStorageDataArrive = (storageNames) => {
            // Update storage value to received one (it may be null).
            if (storageNewOption != null)
                MultiLevelSelectListManager.storageSelectedOption = storageNewOption

            // Update container value to received one (it may be null).
            MultiLevelSelectListManager.containerSelectedOption = containerNewOption

            // Update storage list - HTML, cached values.
            MultiLevelSelectListManager.updateStorages(storageNames)
        }

        let callWhenContainerDataArrive = (containerNames) => {
            // Update storage value to received one (it may be null).
            MultiLevelSelectListManager.containerSelectedOption = containerNewOption

            // Update container list - HTML, cached values.
            MultiLevelSelectListManager.updateContainers(containerNames)
        }

        // Receive all storages from server to ensure chosen one still exists.
        MyApi.Get.Names.storages()
            .then(storageNames => {
                let selectHeader = document.getElementsByClassName("multi-level-select-list")[0]
                selectHeader.replaceChildren()
                callWhenStorageDataArrive(storageNames)

                MyApi.Get.Names.containers(MultiLevelSelectListManager.storageSelectedOption)
                    .then(containerNames => {
                        callWhenContainerDataArrive(containerNames)
                    })

            })
    }
}