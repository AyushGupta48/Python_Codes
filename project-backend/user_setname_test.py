import pytest

import requests
from src.config import url


def test_http_invalid_token(clear_data_http):
    name_change_payload = {
        "token": 0,
        "name_first": "Yeet",
        "name_last": "Max"
    }
    response_user = requests.put(
        f"{url}user/profile/setname/v1", json=name_change_payload).json()

    assert response_user.get('code') == 403


def test_http_empty_name_first(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()
    name_change_payload = {
        "token": response_register.get('token'),
        "name_first": "",
        "name_last": "Mangla"
    }
    response_user = requests.put(
        f"{url}user/profile/setname/v1", json=name_change_payload).json()

    assert response_user.get('code') == 400

# First name > 50


def test_http_name_first_large(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    name_change_payload = {
        "token": response_register.get('token'),
        "name_first": "Djjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj",
        "name_last": "Mangla"
    }
    response_user = requests.put(
        f"{url}user/profile/setname/v1", json=name_change_payload).json()

    assert response_user.get('code') == 400


def test_http_empty_name_last(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    name_change_payload = {
        "token": response_register.get('token'),
        "name_first": "Pranav",
        "name_last": ""
    }
    response_user = requests.put(
        f"{url}user/profile/setname/v1", json=name_change_payload).json()

    assert response_user.get('code') == 400

# Last name > 50


def test_http_name_last_large(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    name_change_payload = {
        "token": response_register.get('token'),
        "name_first": "Pranav",
        "name_last": "Djjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj"
    }
    response_user = requests.put(
        f"{url}user/profile/setname/v1", json=name_change_payload).json()

    assert response_user.get('code') == 400


def test_http_correct_change(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    name_change_payload = {
        "token": response_register.get('token'),
        "name_first": "Pranav",
        "name_last": "Mangla"
    }
    response_user = requests.put(
        f"{url}user/profile/setname/v1", json=name_change_payload).json()

    assert response_user == {}

    user_check = requests.get(
        f"{url}user/profile/v1", params={"token": response_register.get('token'), "u_id": 0}).json()
    assert user_check == {"user": {"u_id": 0, "email": "valid@gmail.com",
                          "name_first": "Pranav", "name_last": "Mangla", "handle_str": "vikramsundar"}}


def test_http_correct_multiple_change(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    name_change_payload = {
        "token": response_register.get('token'),
        "name_first": "Pranav",
        "name_last": "Mangla"
    }
    requests.put(f"{url}user/profile/setname/v1",
                 json=name_change_payload).json()
    user_check = requests.get(
        f"{url}user/profile/v1", params={"token": response_register.get('token'), "u_id": 0}).json()

    assert user_check == {"user": {"u_id": 0, "email": "valid@gmail.com",
                                   "name_first": "Pranav", "name_last": "Mangla", "handle_str": "vikramsundar"}}

    payload_register2 = {
            "email": "valid2@gmail.com",
            "password": "abcdef",
            "name_first": "Daniel",
            "name_last": "Li"
        }
    response_register2 = requests.post(
            f"{url}auth/register/v2", json=payload_register2).json()

    name_change_payload2 = {
            "token": response_register2.get('token'),
            "name_first": "Pranav",
            "name_last": "Mangla"
        }
    requests.put(f"{url}user/profile/setname/v1",
                 json=name_change_payload2).json()

    user_check2 = requests.get(
            f"{url}user/profile/v1", params={"token": response_register2.get('token'), "u_id": 1}).json()
    assert user_check2 == {"user": {"u_id": 1, "email": "valid2@gmail.com",
                                    "name_first": "Pranav", "name_last": "Mangla", "handle_str": "danielli"}}
