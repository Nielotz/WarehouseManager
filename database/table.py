from datetime import datetime

from safrs import SAFRSBase

from . import db


class Storage(SAFRSBase, db.Model):
    __tablename__ = "storages"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text, default='DefaultStorageName')

    supports_includes = False

    # user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<{type(self).__name__}: {self.to_dict()}"

    def to_dict(self):
        return {"name": self.name}


class Container(SAFRSBase, db.Model):
    __tablename__ = "containers"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text, default='DefaultContainerName')
    storage_id = db.Column(db.Integer, db.ForeignKey("storages.id"), nullable=False)

    # created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<{type(self).__name__}: {self.to_dict()}"

    def to_dict(self):
        return {"name": self.name, "storage_id": self.storage_id}


class Item(SAFRSBase, db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text, default='DefaultColumnName')
    barcode = db.Column(db.Text)

    def __repr__(self):
        return f"<{type(self).__name__}: {self.to_dict()}"

    def to_dict(self):
        return {"name": self.name, "barcode": self.barcode}


class ItemHistory(SAFRSBase, db.Model):
    __tablename__ = "items_history"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    container_id = db.Column(db.Integer, db.ForeignKey("containers.id"))
    amount = db.Column(db.Integer)
    amount_unit_id = db.Column(db.Integer, db.ForeignKey("amount_units.id"))
    changed = db.Column(db.DateTime, default=datetime.now().isoformat())
    shop_id = db.Column(db.Integer, db.ForeignKey("shops.id"))

    # prize = db.Column(db.Integer,  -- Stores prize * 100 to avoid float point inaccuracy.
    # changed_by = db.Column(db.Integer,  REFERENCES userdata(user_id)

    def __repr__(self):
        return f"<{type(self).__name__}: {self.to_dict()}"

    def to_dict(self):
        return {
            "id": self.id,
            "item_id": self.item_id,
            "container_id": self.container_id,
            "amount": self.amount,
            "amount_unit_id": self.amount_unit_id,
            "changed": self.changed.isoformat(),
            "shop_id": self.shop_id
        }


class AmountUnit(SAFRSBase, db.Model):
    __tablename__ = "amount_units"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text)
    symbol = db.Column(db.Text)

    def to_dict(self):
        return {"name": self.name, "symbol": self.symbol}


class Shop(SAFRSBase, db.Model):
    __tablename__ = "shops"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text)
    location = db.Column(db.Text)

    def to_dict(self):
        return {"name": self.name, "symbol": self.symbol}
