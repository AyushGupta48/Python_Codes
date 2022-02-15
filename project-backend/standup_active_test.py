import pytest
import requests
from src.config import url
import time

def test_invalid_token(clear_data_http):
    standup_payload = {
        "token": 0,
        "channel_id": 0
    }
    response_user = requests.get(
        f"{url}standup/active/v1", params=standup_payload).json()

    assert response_user.get('code') == 403

def test_http_not_part_of_channel(clear_data_http):
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
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_register2 = requests.post(
        f"{url}auth/register/v2", json=payload_register2).json()

    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    standup_payload = {
        "token": response_register2.get('token'),
        "channel_id": 0,
    }

    response_user = requests.get(
        f"{url}standup/active/v1", params=standup_payload).json()

    assert response_user.get('code') == 403

def test_http_invalid_channel_id(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    standup_payload = {
        "token": response_register.get('token'),
        "channel_id": 900,
    }
    response_user = requests.get(
        f"{url}standup/active/v1", params=standup_payload).json()

    assert response_user.get('code') == 400

def test_http_no_active_standups(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    standup_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
    }
    response_user = requests.get(
        f"{url}standup/active/v1", params=standup_payload).json()

    assert response_user == {
        'is_active': False,
        'time_finish': None
    }

def test_http_one_active_standup(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    standup_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "length": 4
    }
    requests.post(f"{url}standup/start/v1", json=standup_payload).json()

    standup_payload2 = {
        "token": response_register.get('token'),
        "channel_id": 0,
    }
    response_user = requests.get(
        f"{url}standup/active/v1", params=standup_payload2).json()

    assert response_user == {
        'is_active': True,
        'time_finish': int(time.time() + 4)
    }