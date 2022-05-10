from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/main.html')
def main():
    return render_template("main.html")
