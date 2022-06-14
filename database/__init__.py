from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init(app) -> SQLAlchemy:
    """
    Init database.

    :param app: Flask app
    :return: created SQLAlchemy db
    """
    global db
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/warehouse_manager"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

    return db


def recreate():
    db.drop_all()
    db.create_all()
    db.session.commit()
