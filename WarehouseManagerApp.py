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
        @app.route("/api/storages", methods=["GET"])
        def storages():
            storages_from_db: [table.Storage, ] = table.Storage.query.all()
            storages_names = map(lambda storage: storage.name, storages_from_db)
            bleached_storages_names = map(
                lambda name: bleach.clean(text=name, tags=(), attributes={}, protocols=()),
                storages_names
            )
            return jsonify(tuple(bleached_storages_names))

        @staticmethod
        @app.route("/api/storage/<storage>/containers", methods=["GET"])
        def containers(storage):
            return jsonify({"containters": (f"Storage: {storage}", "DummyContainers2", "DummyContainers3")})

        @staticmethod
        @app.route("/api/storage/<storage>/container/<container>/items", methods=["GET"])
        def items(storage, container):
            return jsonify({"items": (f"Storage: {storage}", f"Container: {container}", "DummyItem3")})


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/main.html")
def main():
    return render_template("main.html")
