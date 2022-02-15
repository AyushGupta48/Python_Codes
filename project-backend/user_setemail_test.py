import pytest

import requests
from src.config import url


def test_http_invalid_token(clear_data_http):
    email_change_payload = {
        "token": 0,
        "email": "yeet@gmail.com"
    }
    response_user = requests.put(
        f"{url}user/profile/setemail/v1", json=email_change_payload).json()

    assert response_user.get('code') == 403


def test_http_invalid_email(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    email_change_payload = {
        "token": response_register.get('token'),
        "email": "dingus"
    }
    response_user = requests.put(
        f"{url}user/profile/setemail/v1", json=email_change_payload).json()

    assert response_user.get('code') == 400


def test_http_email_is_used(clear_data_http):
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
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    requests.post(f"{url}auth/register/v2", json=payload_register2).json()

    email_change_payload = {
        "token": response_register.get('token'),
        "email": "valid2@gmail.com"
    }
    response_user = requests.put(
        f"{url}user/profile/setemail/v1", json=email_change_payload).json()

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

    email_change_payload = {
        "token": response_register.get('token'),
        "email": "valid2@gmail.com"
    }
    requests.put(f"{url}user/profile/setemail/v1",
                 json=email_change_payload).json()

    user_check = requests.get(
        f"{url}user/profile/v1", params={"token": response_register.get('token'), "u_id": 0}).json()
    assert user_check == {"user": {"u_id": 0, "email": "valid2@gmail.com",
                          "name_first": "Vikram", "name_last": "Sundar", "handle_str": "vikramsundar"}}


def test_http_correct_multiple_change(clear_data_http):
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
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register2 = requests.post(
        f"{url}auth/register/v2", json=payload_register2).json()

    email_change_payload = {
        "token": response_register.get('token'),
        "email": "valid60@gmail.com"
    }
    requests.put(f"{url}user/profile/setemail/v1",
                 json=email_change_payload).json()
    user_check = requests.get(
        f"{url}user/profile/v1", params={"token": response_register.get('token'), "u_id": 0}).json()

    assert user_check == {"user": {"u_id": 0, "email": "valid60@gmail.com",
                                   "name_first": "Vikram", "name_last": "Sundar", "handle_str": "vikramsundar"}}

    email_change_payload2 = {
            "token": response_register2.get('token'),
            "email": "valid@gmail.com"
        }
    requests.put(f"{url}user/profile/setemail/v1",
                 json=email_change_payload2).json()
    user_check2 = requests.get(
        f"{url}user/profile/v1", params={"token": response_register2.get('token'), "u_id": 1}).json()
    assert user_check2 == {"user": {"u_id": 1, "email": "valid@gmail.com",
                                    "name_first": "Vikram", "name_last": "Sundar", "handle_str": "vikramsundar0"}}


def test_http_empty_email(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    email_change_payload = {
        "token": response_register.get('token'),
        "email": ""
    }
    response_user = requests.put(
        f"{url}user/profile/setemail/v1", json=email_change_payload).json()

    assert response_user.get('code') == 400


def test_http_channel_email_change(clear_data_http):
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
        "name_first": "Doink",
        "name_last": "Leings"
    }
    response_register2 = requests.post(
        f"{url}auth/register/v2", json=payload_register2).json()

    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    join_payload = {
        "token": response_register2.get("token"),
        "channel_id": 0
    }
    requests.post(f"{url}channel/join/v2", json=join_payload)

    payload_create_channel2 = {
        "token": response_register2.get('token'),
        "name": "dingus",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel2)

    email_change_payload = {
        "token": response_register.get('token'),
        "email": "dingus@gmail.com"
    }
    requests.put(f"{url}user/profile/setemail/v1",
                 json=email_change_payload).json()

    user_check = requests.get(
        f"{url}user/profile/v1", params={"token": response_register.get('token'), "u_id": 0}).json()

    assert user_check.get("user")["email"] == "dingus@gmail.com"
