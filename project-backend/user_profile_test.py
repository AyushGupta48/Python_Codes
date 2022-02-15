import pytest

import requests
from src.config import url


def test_http_invalid_token(clear_data_http):
    response_user = requests.get(
        f"{url}user/profile/v1", params={"token": 0, "u_id": 0}).json()

    assert response_user.get('code') == 403


def test_http_invalid_uid(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    response_user = requests.get(
        f"{url}user/profile/v1", params={"token": response_register.get('token'), "u_id": "1"}).json()

    assert response_user.get('code') == 400


def test_http_single_user(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()
    response_user = requests.get(
        f"{url}user/profile/v1", params={"token": response_register.get('token'), "u_id": 0}).json()

    assert response_user == {"user": {"u_id": 0, "email": "valid@gmail.com",
                             "name_first": "Vikram", "name_last": "Sundar", "handle_str": "vikramsundar"}}


def test_http_multiple_users(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
        }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    payload_register2 = {
        "email": "valid2@gmail.com",
        "password": "abcdef",
        "name_first": "Pranav",
        "name_last": "Mangla"
        }
    requests.post(f"{url}auth/register/v2", json=payload_register2).json()

    payload_register3 = {
        "email": "valid3@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
        }
    requests.post(f"{url}auth/register/v2", json=payload_register3).json()

    response_user_list = requests.get(
        f"{url}user/profile/v1", params={"token": response_register.get('token'), "u_id": 2}).json()

    assert response_user_list == {"user": {"u_id": 2, "email": "valid3@gmail.com",
                                           "name_first": "Vikram", "name_last": "Sundar", "handle_str": "vikramsundar0"}}
