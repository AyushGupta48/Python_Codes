import pytest
from src.other import clear_v1
import requests
from src.config import url


@pytest.fixture
def clear_data():
    return clear_v1()


@pytest.fixture
def clear_data_http():
    return requests.delete(url + "clear/v1")
