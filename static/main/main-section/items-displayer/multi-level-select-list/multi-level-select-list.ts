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
    static Thing = class {
        id: number
        name: string
    }

    static Storage = class extends MyApi.Thing {
    }

    static Container = class extends MyApi.Thing {
    }

    static Get = class {
        static storages() {
            return MyApi.Get.ask_for("api/storages")
        }

        static containers(storageId: number) {
            return MyApi.Get.ask_for(`api/storages/${storageId}/containers`)
        }

        static items(storageId: number, containerId: number) {
            return MyApi.Get.ask_for(`api/storages/${storageId}/containers/${containerId}/items`)
        }

        private static ask_for(path: string) {
            return Api.get<InstanceType<typeof MyApi.Thing>>(path)
        }
    }
}


abstract class MultiLevelSelectListManager {
    static Storages: Array<InstanceType<typeof MyApi.Storage>>

    // In case null in selectedOption - select first one.
    private static generateSelectElementHtml(htmlElementIdName: string, selected: InstanceType<typeof MyApi.Thing>,
                                             optionsIdName: Array<{ id: number, name: string }>, onChange: string) {
        let openingHtml = `<label for="${htmlElementIdName}"></label>\n` +
            `<select id="${htmlElementIdName}" name="${htmlElementIdName}" ` +
            `class="my-selector" onchange="${onChange}">`

        let optionsHtml = optionsIdName.map(option => {
            if (selected !== null && selected.id === option.id)
                return `  <option value=${option.id} selected>${option.name.toUpperCase()}</option>`
            else
                return `  <option value=${option.id}>${option.name.toUpperCase()}</option>`
        })
        let closingHtml = '</select>'

        return openingHtml + "\n" + optionsHtml.join("\n") + "\n" + closingHtml + "\n"
    }

    // Overwrite storages section in HTMl.
    private static updateStorages(storages: Array<InstanceType<typeof MyApi.Storage>>,
                                  selected: InstanceType<typeof MyApi.Storage> = null) {
        if (selected === null && storages.length)
            selected = storages[0]
        let selectElementCode: string =
            MultiLevelSelectListManager.generateSelectElementHtml("my-selector-storage",
                selected,
                storages,
                "MultiLevelSelectListManager.update(value, null)")
        let header = document.getElementsByClassName("multi-level-select-list")[0]
        header.insertAdjacentHTML("beforeend", selectElementCode)
    }

    // Overwrite containers section in HTMl.
    private static updateContainers(containers: Array<InstanceType<typeof MyApi.Container>>,
                                    selected: InstanceType<typeof MyApi.Container> = null) {
        if (selected === null && containers.length)
            selected = containers[0]

        let selectElementCode: string =
            MultiLevelSelectListManager.generateSelectElementHtml("my-selector-container",
                selected,
                containers,
                "MultiLevelSelectListManager.update(this.parentElement.querySelector('#my-selector-storage').value, value)")
        let header = document.getElementsByClassName("multi-level-select-list")[0]
        header.insertAdjacentHTML("beforeend", selectElementCode)
    }

    // Update MultiLevelSelectList (modifies HTML).
    static update(selectedStorageId: number = null, selectedContainerId: number = null) {
        if (selectedStorageId !== null)
            selectedStorageId = Number(selectedStorageId)
        if (selectedContainerId !== null)
            selectedContainerId = Number(selectedContainerId)

        let callWhenStorageDataArrive = (storages) => {
            let selectedStorage: InstanceType<typeof MyApi.Storage> = null

            if (selectedStorageId !== null) {
                let selectedStorage_ = storages.filter(storage => storage.id === selectedStorageId)
                if (selectedStorage_.length) {
                    selectedStorage = selectedStorage_[0]
                } else {
                    // TODO: Error handling: selected option does not exists in database.
                    alert(`Selected storage_id(${selectedStorageId}) does not exists in db.`)
                }
            } else if (storages.length) {
                selectedStorage = storages[0]
            }

            // Update storage list - HTML, cached values.
            MultiLevelSelectListManager.updateStorages(storages, selectedStorage)

            return selectedStorage
        }

        let callWhenContainerDataArrive = (containers) => {
            // Update container list - HTML, cached values.
            let selectedContainer: InstanceType<typeof MyApi.Container> = null
            if (selectedContainerId !== null) {
                let selectedContainer_ = containers.filter(container => container.id === selectedContainerId)
                if (selectedContainer_.length) {
                    selectedContainer = selectedContainer_[0]
                } else {
                    // TODO: Error handling: selected option does not exists in database.
                    alert(`Selected container_id(${selectedContainerId}) does not exists in db.`)
                }
            } else if (containers.length) {
                selectedContainer = containers[0]
            }

            MultiLevelSelectListManager.updateContainers(containers, selectedContainer)
        }

        // Receive all storages from server to ensure chosen one still exists.
        MyApi.Get.storages()
            .then(storages => {
                let selectHeader = document.getElementsByClassName("multi-level-select-list")[0]
                selectHeader.replaceChildren()
                let selectedStorage = callWhenStorageDataArrive(storages)

                MyApi.Get.containers(selectedStorage.id)
                    .then(containers => {
                        callWhenContainerDataArrive(containers)
                    })

            })
    }
}