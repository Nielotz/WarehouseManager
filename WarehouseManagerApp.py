from flask import Flask, jsonify
from flask import render_template

app = Flask(__name__)


class RestApi:
    class Get:
        @staticmethod
        @app.route("/api/storages_names", methods=["GET"])
        def storages_names():
            return jsonify({"names": ("DummyStorage1", "DummyStorage2", "DummyStorage3")})

        @staticmethod
        @app.route("/api/storage/<storage>/containers_names", methods=["GET"])
        def containers_names(storage):
            return jsonify({"names": (f"Storage: {storage}", "DummyContainers2", "DummyContainers3")})

        @staticmethod
        @app.route("/api/storage/<storage>/container/<container>/items_names", methods=["GET"])
        def items_names(storage, container):
            return jsonify({"names": (f"Storage: {storage}", f"Container: {container}", "DummyItem3")})

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
