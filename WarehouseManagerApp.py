import bleach
from flask import Flask, jsonify
from flask import render_template

import database
from database import table

app = Flask(__name__)

db = database.init(app)


def extract_and_bleach(items: [], key: callable) -> [str, ]:
    return [bleach.clean(text=key(item), tags=(), attributes={}, protocols=()) for item in items]


class RestApi:
    class Get:
        @staticmethod
        @app.route("/api/storages", methods=["GET"])
        def storages():
            storages_data: [table.Storage, ] = table.Storage.query.all()
            # TODO: Security - add sanitization.
            # TODO: Security - add fields whitelist.
            return jsonify([sd.to_dict() for sd in storages_data])

        @staticmethod
        @app.route("/api/storages/<int:storage_id>/containers", methods=["GET"])
        def containers(storage_id: int):
            # TODO [Refactor]: Try to do this in one call
            storage_data: table.Storage = table.Storage.query.filter_by(id=storage_id).first()

            if storage_data is None:
                return jsonify({})

            containers_data: [table.Container, ] = table.Container.query \
                .join(table.Storage, table.Container.storage_id == table.Storage.id) \
                .filter(storage_data.id == table.Container.storage_id).all()

            return jsonify([cd.to_dict() for cd in containers_data])

        @staticmethod
        @app.route("/api/storages/<int:storage_id>/containers/<int:container_id>/items_history", methods=["GET"])
        def items_history(storage_id: int, container_id: int):
            # TODO [Refactor]: Try to do this in one call
            storage_data: table.Storage = table.Storage.query.filter_by(id=storage_id).first()

            if storage_data is None:
                return jsonify({})

            container_data: [table.Container, ] = table.Container.query \
                .join(table.Storage, table.Container.storage_id == table.Storage.id) \
                .filter(storage_data.id == table.Container.storage_id) \
                .filter_by(id=container_id).first()

            if container_data is None:
                return jsonify({})

            items_history_: [table.ItemHistory, ] = table.ItemHistory.query \
                .join(table.Container, table.ItemHistory.container_id == table.Container.id) \
                .filter(container_data.id == table.Container.id).all()

            if container_data is None:
                return jsonify({})

            return jsonify([ih.to_dict() for ih in items_history_])

        @staticmethod
        @app.route("/api/items", methods=["GET"])
        def items():
            # TODO [Refactor]: Try to do this in one call
            items_data: [table.Item, ] = table.Item.query.all()

            if items_data is None:
                return jsonify({})

            return jsonify([item.to_dict() for item in items_data])

        @staticmethod
        @app.route("/api/amount_units", methods=["GET"])
        def amount_units():
            # TODO [Refactor]: Try to do this in one call
            amount_units_data: [table.Item, ] = table.Item.query.all()

            if amount_units_data is None:
                return jsonify({})

            return jsonify([unit.to_dict() for unit in amount_units_data])

        @staticmethod
        @app.route("/api/shops", methods=["GET"])
        def shops():
            # TODO [Refactor]: Try to do this in one call
            shops: [table.Shop, ] = table.Shop.query.all()

            if shops is None:
                return jsonify({})

            return jsonify([shop.to_dict() for shop in shops])


RestApi.Get.items_history(1, 1)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/main.html")
def main():
    return render_template("main.html")
