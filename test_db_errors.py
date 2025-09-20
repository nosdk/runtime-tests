from requests import get, post


# def test_duplicate_records(table):
#     item = {
#         "id": 123,
#         "name": "tim",
#     }
#
#     resp = post(table, json=item)
#     assert resp.status_code == 200
#
#     resp = post(table, json=item)
#     assert resp.status_code == 409
