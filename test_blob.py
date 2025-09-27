import os
from requests import get, put

NOSDK = os.getenv("NOSDK")

bucket = f"{NOSDK}/blob/nosdk.test"


def test_get_and_put():
    path = f"{bucket}/hello.txt"
    data = "hello from my file\n"

    resp = put(path, data=data)
    assert resp.status_code == 200

    resp = get(path)
    assert resp.status_code == 200
    assert resp.text == data
