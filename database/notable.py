# noinspection PyMethodParameters
import json

import safrs.util
from safrs import SAFRSBase
from safrs.safrs_types import SAFRSID

# noinspection PyMethodMayBeStatic,PyMethodParameters
import redis_api


class AllItemChangesQuery:
    """
    The safrs sqla serialization calls some sqlalchemy methods
    We emulate them here
    """

    def first(cls):
        return AllItemChanges()

    def filter_by(cls, *args, **kwargs):
        return cls

    def count(cls, *args, **kwargs):
        return 100

    def offset(cls, offset):
        return cls

    def limit(cls, limit):
        return cls

    def all(cls):
        all_ = []
        keys = redis_api.get_all_keys(prefix="WMA_")
        for key in keys:
            data_status, data = AllItemChanges.get_data_status_and_data(key=key)
            all_.append(AllItemChanges(redis_key=key, data_status=data_status, data=data))

        return all_

    def order_by(cls, attr_name):
        return cls


# noinspection PyMethodParameters
class AllItemChanges(SAFRSBase):
    """
    description: Request and receive all items changes within specified container.
    """

    @property
    def _s_auto_commit(self):
        return False

    __tablename__ = "all_item_changes"  # Endpoint name

    _id: str = "redis_key"
    id_type = SAFRSID
    _data_status: ""
    _data: ""
    _item_id: int = 0
    _container_id: int = 0
    exclude_attrs = ["id"]
    http_methods = ["get", "post"]

    def __new__(cls, *args, **kwargs):
        """
        override SAFRSBase.__new__
        """
        return object.__new__(cls)

    # noinspection PyMissingConstructor
    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
        self._item_id = kwargs["item_id"] if "item_id" in kwargs else ""
        self._container_id = kwargs["container_id"] if "container_id" in kwargs else ""
        self._id = kwargs["redis_key"] if "redis_key" in kwargs else ""
        self._data_status, self._data = AllItemChanges.get_data_status_and_data(key=self._id)

    @staticmethod
    def get_data_status_and_data(key) -> (bytes, {}):
        value: bytes = redis_api.get(key)
        data: {} = {}
        if value is None:
            return b"Not exists", {}
        if value == b"In progress":
            data_status = "In progress"
        else:
            data_status = "Done"
            data = json.loads(value)
        return data_status, data

    @safrs.util.classproperty
    def _s_query(cls):
        """
        query placeholder
        """
        return AllItemChangesQuery()

    @safrs.util.classproperty
    def _s_relationships(cls):
        """
        return the included relationships
        """
        return {}

    @safrs.jsonapi_attr
    def name(self):
        return "all_item_changes"

    @safrs.jsonapi_attr
    def item_id(self) -> int:
        return self._item_id

    @safrs.jsonapi_attr
    def id(self) -> str:
        return self._id

    @safrs.jsonapi_attr
    def container_id(self) -> int:
        return self._container_id

    @safrs.jsonapi_attr
    def data_status(self):
        return self._data_status

    @safrs.jsonapi_attr
    def data(self):
        return self._data

    # noinspection PyMethodOverriding,PyShadowingBuiltins
    @classmethod
    def get_instance(cls, id, failsafe=False):
        """
        return the instance specified by id
        """
        return AllItemChanges(redis_key=id)

    @safrs.util.classproperty
    def class_(cls):
        return cls

    @classmethod
    def _s_get(cls, **kwargs):
        """
        This method is called when a collection is requested with a HTTP GET to the json api
        """
        return cls.jsonapi_filter()

    @classmethod
    def _s_post(cls, jsonapi_id=None, **params):
        """
        This method is called when a new item is created with a POST to the json api

        :param attributes: the jsonapi "data" attributes
        :return: new `cls` instance

        `_s_post` performs attribute sanitization and calls `cls.__init__`
        The attributes may contain an "id" if `cls.allow_client_generated_ids` is True
        """
        # remove attributes that are not declared in _s_jsonapi_attrs
        attributes = {attr_name: params[attr_name] for attr_name in params if attr_name in cls._s_jsonapi_attrs}

        # Create the object instance with the specified id and json data
        # If the instance (id) already exists, it will be updated with the data
        # pylint: disable=not-callable
        instance = cls(**attributes)

        instance._add_rels(**params)

        instance._data_status = "In progress"
        instance._id = redis_api.schedule_get_all_item_changes(item_id=instance.item_id,
                                                               container_id=instance.container_id)

        return instance

    def to_dict(self, *args, **kwargs):
        return {
            "id": self._id,
            "item_id": self.item_id,
            "container_id": self.container_id,
            "data_status": self._data_status,
            "data": self._data,
        }