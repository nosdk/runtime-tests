import pytest
import random
import string
from os import getenv

NOSDK = getenv("NOSDK")


def random_suffix(s: str) -> str:
    suffix = "".join(random.choices(string.ascii_letters, k=10))
    return f"{s}_{suffix}"


@pytest.fixture(scope="function")
def table(request):
    table_name = random_suffix(request.node.name)
    return f"{NOSDK}/db/{table_name}"
