from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from . import table, db


@contextmanager
def session(*args):
    session_ = sessionmaker(bind=db.engine)()
    try:
        yield session_
    finally:
        session_.close()


def get_storage_by_id(storage_id: int):
    return table.Storage.query.filter(id=storage_id).all()


def get_container_by_id(storage_id: int, container_id: int):
    return table.Storage.query.filter(
        table.Storage.storage_id == storage_id,
        table.Storage.id == container_id
    ).all()


def get_all_item_changes(item_id: int, container_id: int):
    with session() as session_:
        tih = table.ItemHistory
        return session_.query(tih).filter(
            tih.item_id == item_id,
            tih.container_id == container_id,
        ).all()


def fill_with_sample_data():
    item_101: table.Item = table.Item(name="TestItem101", barcode="TestItem101Barcode")
    item_102: table.Item = table.Item(name="TestItem102", barcode="TestItem102Barcode")
    item_103: table.Item = table.Item(name="TestItem103", barcode="TestItem103Barcode")

    shop_1: table.Shop = table.Shop(name="TestShop1")
    shop_2: table.Shop = table.Shop(name="TestShop2")
    shop_3: table.Shop = table.Shop(name="TestShop3")

    amount_unit_1: table.AmountUnit = table.AmountUnit(name="TestAmountUnit1", symbol="TestAmountUnit1ASymbol")
    amount_unit_2: table.AmountUnit = table.AmountUnit(name="TestAmountUnit2", symbol="TestAmountUnit2ASymbol")
    amount_unit_3: table.AmountUnit = table.AmountUnit(name="TestAmountUnit3", symbol="TestAmountUnit3ASymbol")

    storage_100: table.Storage = table.Storage(name="TestStorage100")

    container_110: table.Container = table.Container(storage_id=storage_100.id, name="TestContainer110")

    for i in range(5):
        table.ItemHistory(
            item_id=item_101.id,
            container_id=container_110.id,
            amount=i,
            amount_unit_id=amount_unit_1.id,
            shop_id=shop_1.id
        ),
        table.ItemHistory(
            item_id=item_102.id,
            container_id=container_110.id,
            amount=i,
            amount_unit_id=amount_unit_1.id,
            shop_id=shop_1.id
        )

    container_120: table.Container = table.Container(storage_id=storage_100.id, name="TestContainer120")
    container_130: table.Container = table.Container(storage_id=storage_100.id, name="TestContainer130")
