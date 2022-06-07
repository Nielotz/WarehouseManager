from datetime import datetime

from . import db


class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text, default='DefaultColumnName')

    # user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<{type(self).__name__}: id={self.id}, name={self.name}>"

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text, default='DefaultContainerName')
    storage_id = db.Column(db.Integer, db.ForeignKey("storage.id"), nullable=False)

    # created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<{type(self).__name__}: id={self.id}, name={self.name}, storage_id={self.storage_id}>"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "storage_id": self.storage_id}


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text, default='DefaultColumnName')
    barcode = db.Column(db.Text)

    def __repr__(self):
        return f"<{type(self).__name__}: id={self.id}, name={self.name}, barcode={self.barcode}>"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "barcode": self.barcode}


class ItemHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"), nullable=False)
    amount = db.Column(db.Integer)
    # amount_unit = db.Column(db.Int,  REFERENCES amount_unit,
    changed = db.Column(db.DateTime, default=datetime.now().isoformat())

    # prize = db.Column(db.Integer,  -- Stores real prize * 100 to avoid float point inaccuracy.
    # shop_id = db.Column(db.Integer,  REFERENCES shop(shop_id),
    # changed_by = db.Column(db.Integer,  REFERENCES userdata(user_id)

    def __repr__(self):
        return f"<{type(self).__name__}: " \
               f"id={self.id}, item_id={self.item_id}, amount={self.amount}, changed={self.changed}>"

    def to_dict(self):
        return {"id": self.id, "item_id": self.item_id, "amount": self.amount, "changed": self.changed}
