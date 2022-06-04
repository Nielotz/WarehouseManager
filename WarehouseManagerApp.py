from flask import Flask, jsonify
from flask import render_template
import bleach

import database
from database import table

app = Flask(__name__)

db = database.init(app)


class RestApi:
    class Get:
        @staticmethod
        @app.route("/api/storages_names", methods=["GET"])
        def storages_names():
            storages_from_db: [table.Storage, ] = table.Storage.query.all()
            storages_names = map(lambda storage: storage.name, storages_from_db)
            bleached_storages_names = map(
                lambda name: bleach.clean(text=name, tags=(), attributes={}, protocols=()),
                storages_names
            )
            return jsonify({"names": tuple(bleached_storages_names)})

        @staticmethod
        @app.route("/api/storage/<storage>/containers_names", methods=["GET"])
        def containers_names(storage):
            return jsonify({"names": (f"Storage: {storage}", "DummyContainers2", "DummyContainers3")})

        @staticmethod
        @app.route("/api/storage/<storage>/container/<container>/items_names", methods=["GET"])
        def items_names(storage, container):
            return jsonify({"names": (f"Storage: {storage}", f"Container: {container}", "DummyItem3")})


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/main.html")
def main():
    return render_template("main.html")
