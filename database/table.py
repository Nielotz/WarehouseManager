from datetime import datetime

from . import db


class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text, default='DefaultColumnName')

    # user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<{type(self).__name__}: {self.to_dict()}"

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text, default='DefaultContainerName')
    storage_id = db.Column(db.Integer, db.ForeignKey("storage.id"), nullable=False)

    # created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<{type(self).__name__}: {self.to_dict()}"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "storage_id": self.storage_id}


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text, default='DefaultColumnName')
    barcode = db.Column(db.Text)

    def __repr__(self):
        return f"<{type(self).__name__}: {self.to_dict()}"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "barcode": self.barcode}


class ItemHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"), nullable=False)
    container_id = db.Column(db.Integer, db.ForeignKey("container.id"))
    amount = db.Column(db.Integer)
    amount_unit = db.Column(db.Integer, db.ForeignKey("amount_unit.id"))
    changed = db.Column(db.DateTime, default=datetime.now().isoformat())
    shop_id = db.Column(db.Integer, db.ForeignKey("shop.id"))

    # prize = db.Column(db.Integer,  -- Stores prize * 100 to avoid float point inaccuracy.
    # changed_by = db.Column(db.Integer,  REFERENCES userdata(user_id)

    def __repr__(self):
        return f"<{type(self).__name__}: {self.to_dict()}"

    def to_dict(self):
        return {"id": self.id, "item_id": self.item_id, "amount": self.amount, "changed": self.changed}


class AmountUnit(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text)
    symbol = db.Column(db.Text)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "symbol": self.symbol}


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text)
    location = db.Column(db.Text)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "symbol": self.symbol}
