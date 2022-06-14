import json
import random
import string
import threading
from time import sleep

import redis as redis

import database.api

redis_ = redis.Redis(host='localhost', port=6379, db=0)


def schedule_get_all_item_changes(item_id: int, container_id: int) -> str:
    def _get_all_item_changes(item_id_: int, container_id_: int, redis_key: str):
        redis_.set(name=redis_key, value="In progress")
        item_changes = database.api.get_all_item_changes(item_id_, container_id_)
        redis_.set(name=redis_key, value=json.dumps([ic.to_dict() for ic in item_changes]))

    key = get_random_free_key(prefix=f"WMA_{container_id}_{item_id}_")
    
    threading.Thread(
        target=_get_all_item_changes,
        args=(item_id, container_id, key),
        daemon=True
    ).start()

    return key


def get_random_free_key(prefix="") -> str:
    while True:
        key = prefix + "".join(random.choices(string.ascii_lowercase, k=70))
        if not redis_.exists(key):
            return key


def get(key: str):
    return redis_.get(name=key)


def get_all_keys(prefix=""):
    return [key for key in redis_.scan_iter(match=f"{prefix}*")]
