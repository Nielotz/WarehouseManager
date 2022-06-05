import bleach
from flask import Flask, jsonify
from flask import render_template

import database
from database import table

app = Flask(__name__)

db = database.init(app)


def extract_and_bleach(items: [], sub_item_getter: callable) -> [str, ]:
    return [bleach.clean(text=sub_item_getter(item), tags=(), attributes={}, protocols=()) for item in items]


class RestApi:
    class Get:
        @staticmethod
        @app.route("/api/storages", methods=["GET"])
        def storages():
            storages_data: [table.Storage, ] = table.Storage.query.all()  # TODO: Optimize - query only names.
            # TODO: Security - add sanitization.
            # TODO: Security - add fields whitelist.
            return jsonify([sd.to_dict() for sd in storages_data])

        @staticmethod
        @app.route("/api/storages/<int:storage_id>/containers", methods=["GET"])
        def containers(storage_id: int):
            # TODO: Optimize - query only names.
            storage_data: table.Storage = table.Storage.query.filter_by(id=storage_id).first()

            if storage_data is None:
                return jsonify({})

            containers_data: [table.Container, ] = table.Container.query \
                .join(table.Storage, table.Container.storage_id == table.Storage.id) \
                .filter(storage_data.id == table.Container.storage_id).all()

            return jsonify([cd.to_dict() for cd in containers_data])

        @staticmethod
        @app.route("/api/storages/<int:storage_id>/containers/<int:container_id>/items", methods=["GET"])
        def items(storage_id: int, container_id: int):
            return jsonify({"names": (f"Storage: {storage_id}", f"Container: {container_id}", "DummyItem3")})


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/main.html")
def main():
    return render_template("main.html")
