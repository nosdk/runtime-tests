import os
from requests import get, post

NOSDK = os.getenv("NOSDK")

test_topic = f"{NOSDK}/msg/nosdk-test"
empty_topic = f"{NOSDK}/msg/nothing"


def test_pub_sub():
    msg = {"name": "tim"}

    resp = post(test_topic, json=msg)
    assert resp.status_code == 200

    resp = get(test_topic)
    assert resp.status_code == 200
    assert resp.json()["name"] == "tim"


# def test_no_messages():
#     message = get(empty_topic).json()
#     assert message is None
