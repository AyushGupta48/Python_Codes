import pytest
import requests
from src.config import url
from src.auth import auth_register_v2, create_handle

# Test a normal handle is being added correctly to the datastore


def test_normal_handle(clear_data):
    assert create_handle("Pranav", "Mangla") == 'pranavmangla'

# Test a first name and last name with non-alphanumeric characters


def test_non_alphanumeric(clear_data):
    assert create_handle("Pr@n@v", "M!ngla") == 'prnvmngla'

# Test a handle when given long name


def test_long_name(clear_data):
    assert create_handle(
        "Pranav", "abcdefghijklmnopqrstuvwxyz") == 'pranavabcdefghijklmn'

# Test a handle when given a long name on edge case


def test_long_name_again(clear_data):
    assert create_handle(
        "abcdef", "ghijklmnopqrstuvwxyz") == 'abcdefghijklmnopqrst'

# Test a handle when the handle is same as one existing one


def test_duplicate_one(clear_data):
    auth_register_v2("valid@gmail.com", "yeeticus", "Pranav", "Mangla")

    assert create_handle("Pranav", "Mangla") == 'pranavmangla0'

# Test a handle when the handle is the same as two existing ones


def test_duplicate_two(clear_data):
    auth_register_v2("valid@gmail.com", "yeeticus", "Pranav", "Mangla")
    auth_register_v2("validanother@gmail.com", "yeeticus", "Pranav", "Mangla")

    assert create_handle("Pranav", "Mangla") == 'pranavmangla1'

# Test adding multiple users but with different people each time


def test_duplicate_with_intermediate(clear_data):
    auth_register_v2("valid@gmail.com", "yeeticus", "Pranav", "Mangla")
    auth_register_v2("validanother@gmail.com", "yeeticus", "Daniel", "Li")

    assert create_handle("Pranav", "Mangla") == 'pranavmangla0'
    assert create_handle("Daniel", "Li") == 'danielli0'

# Test even more users


def test_more_duplicates(clear_data):
    auth_register_v2("valid@gmail.com", "yeeticus", "Pranav", "Mangla")

    assert create_handle("Daniel", "Li") == 'danielli'

    auth_register_v2("validanotherp@gmail.com", "yeeticus", "Daniel", "Li")
    auth_register_v2("valids@gmail.com", "yeeticus", "Pranav", "Mangla")
    auth_register_v2("validity@gmail.com", "yeeticus", "Ayush", "Gupta")

    assert create_handle("Ayush", "Gupta") == 'ayushgupta0'

    auth_register_v2("validanothers@gmail.com", "yeeticus", "Daniel", "Li")
    assert create_handle("Pranav", "Mangla") == 'pranavmangla1'


def test_empty(clear_data):
    assert create_handle("!@#$%-=", "!@#$%-=") == ''


def test_empty_duplicate(clear_data):
    auth_register_v2("valid@gmail.com", "yeeticis", "!@#$%-=", "!@#$%-=")

    assert create_handle("!@#$%-=", "!@#$%-=") == ''


def test_more_empty(clear_data):
    auth_register_v2("valid@gmail.com", "yeeticus", "Pranav", "Mangla")

    assert create_handle("Daniel", "Li") == 'danielli'

    auth_register_v2("validing@gmail.com", "yeeticis", "!@#$%-=", "!@#$%-=")

    assert create_handle("!@#$%-=", "!@#$%-=") == ''

    auth_register_v2("validanotherp@gmail.com", "yeeticus", "Daniel", "Li")
    auth_register_v2("valids@gmail.com", "yeeticus", "Pranav", "Mangla")
    auth_register_v2("validity@gmail.com", "yeeticus", "Ayush", "Gupta")

    assert create_handle("Ayush", "Gupta") == 'ayushgupta0'

    auth_register_v2("validanothers@gmail.com", "yeeticus", "Daniel", "Li")

    assert create_handle("Pranav", "Mangla") == 'pranavmangla1'

    auth_register_v2("validpingu@gmail.com", "yeeticis", "!@#$%-=", "!@#$%-=")

    assert create_handle("!@#$%-=", "!@#$%-=") == ''


def test_http_empty(clear_data_http):
    payload = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "!@#$%-=",
        "name_last": "@#$%-="
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload).json()

    response_user = requests.get(
        f"{url}user/profile/v1", params={"token": response_register.get('token'), "u_id": 0}).json()
    assert response_user.get("user")["handle_str"] == ''


def test_http_handle_too_long(clear_data_http):
    payload = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Pranav",
        "name_last": "abcdefghijklmnopqrstuvwxyz"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload).json()

    response_user = requests.get(
        f"{url}user/profile/v1", params={"token": response_register.get('token'), "u_id": 0}).json()
    assert response_user.get("user")["handle_str"] == "pranavabcdefghijklmn"
