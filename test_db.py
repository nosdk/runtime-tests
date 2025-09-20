from requests import get, post, put, delete
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
    put(table, json=item)

    res = get(table).json()

    assert len(res) == 1
    assert res[0]["name"] == "jim"


def test_update_no_id(table):
    item = {
        "name": "tim",
    }

    post(table, json=item)

    res = get(table).json()
    assert len(res) == 1
    assert "id" in res[0]

    res[0]["name"] = "jim"
    put(table, json=res[0])
    print("posted", res[0])

    res = get(table).json()
    assert len(res) == 1
    assert res[0]["name"] == "jim"


def test_get_by_id(table):
    item = {
        "id": str(uuid4()),
        "name": "tim",
    }

    post(table, json=item)

    res = get(f"{table}/{item['id']}").json()
    assert res["id"] == item["id"]


def test_delete_by_id(table):
    item = {
        "id": str(uuid4()),
        "name": "tim",
    }

    item2 = {
        "id": str(uuid4()),
        "name": "jim",
    }

    post(table, json=[item, item2])
    assert len(get(table).json()) == 2

    resp = delete(f"{table}/{item['id']}")
    assert resp.status_code == 200

    res = get(table).json()
    assert len(res) == 1
    assert res[0]["name"] == "jim"


def test_delete_by_query(table):
    items = [
        {"name": "tim", "age": 35},
        {"name": "jim", "age": 61},
        {"name": "george", "age": 71},
    ]

    post(table, json=items)
    assert len(get(table).json()) == 3

    resp = delete(f"{table}?age>60")
    assert resp.status_code == 200

    res = get(table).json()
    assert len(res) == 1
    assert res[0]["name"] == "tim"
