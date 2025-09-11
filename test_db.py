from requests import get, post
from uuid import uuid4


def test_post_basic(table):
    num_items = 5
    for i in range(num_items):
        data = {"item": i, "uuid": str(uuid4())}
        resp = post(table, json=data)
        assert resp.status_code == 200

    items = get(table).json()
    assert len(items) == num_items


def test_post_array(table):
    items = [
        {"name": "tim", "uuid": str(uuid4())},
        {"name": "paul"},
    ]

    resp = post(table, json=items)
    assert resp.status_code == 200

    res = get(table).json()
    assert len(res) == 2


def test_query_basic(table):
    items = [
        {"name": "tim"},
        {"name": "jim"},
    ]

    for item in items:
        post(table, json=item)

    res = get(f"{table}?name=jim").json()
    assert len(res) == 1
    assert res[0]["name"] == "jim"

    res = get(f"{table}?name=paul").json()
    assert len(res) == 0


def test_query_numeric(table):
    for i in range(100):
        post(table, json={"num": i})

    items = get(f"{table}?num<10").json()
    assert len(items) == 10
    for item in items:
        assert item["num"] < 10


def test_not_query(table):
    items = [
        {"name": "tim"},
        {"name": "jim"},
    ]

    post(table, json=items)

    res = get(f"{table}?name!tim").json()
    assert len(res) == 1
    assert res[0]["name"] == "jim"


def test_boolean_query(table):
    items = [
        {"valid": True},
        {"valid": False},
    ]

    post(table, json=items)

    res = get(f"{table}?valid=true").json()
    assert len(res) == 1
    assert res[0]["valid"]


def test_update_record(table):
    item = {
        "id": str(uuid4()),
        "name": "tim",
    }

    post(table, json=item)
    item["name"] = "jim"
    post(table, json=item)

    res = get(table).json()

    assert len(res) == 1
    assert res[0]["name"] == "jim"
