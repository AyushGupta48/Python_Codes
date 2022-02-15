import pytest
import requests
from src.config import url


def test_http_invalid_token(clear_data_http):

    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    payload_leave_channel = {
        "token": 'thisiswrongrtoken',
        "channel_id": response_channel_data.get('channel_id')
    }

    response_leave_channel = requests.post(
        f"{url}channel/leave/v1", json=payload_leave_channel)
    response_leave_channel_data = response_leave_channel.json()

    assert response_leave_channel_data.get('code') == 403


def test_http_not_a_member(clear_data_http):

    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_user_2 = {
        "email": "valid2@gmail.com",
        "password": "alkdjnfklasd",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_user2 = requests.post(
        f"{url}auth/register/v2", json=payload_user_2)
    response_user2_data = response_user2.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    payload_leave_channel = {
        "token": response_user2_data.get('token'),
        "channel_id": response_channel_data.get('channel_id')
    }

    response_leave_channel = requests.post(
        f"{url}channel/leave/v1", json=payload_leave_channel)
    response_leave_channel_data = response_leave_channel.json()

    assert response_leave_channel_data.get('code') == 403


def test_http_invalid_channel_id(clear_data_http):

    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    payload_leave_channel = {
        "token": response_user_data.get('token'),
        "channel_id": 123897
    }

    response_leave_channel = requests.post(
        f"{url}channel/leave/v1", json=payload_leave_channel)
    response_leave_channel_data = response_leave_channel.json()

    assert response_leave_channel_data.get('code') == 400


def test_http_already_left(clear_data_http):

    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_user_2 = {
        "email": "valid2@gmail.com",
        "password": "alkdjnfklasd",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_user2 = requests.post(
        f"{url}auth/register/v2", json=payload_user_2)
    response_user2_data = response_user2.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    payload_user2_joining_channel = {
        "token": response_user2_data.get('token'),
        "channel_id": response_channel_data.get('channel_id')
    }

    requests.post(f"{url}channel/join/v2", json=payload_user2_joining_channel)

    payload_leave_channel = {
        "token": response_user2_data.get('token'),
        "channel_id": response_channel_data.get('channel_id')
    }

    response_leave_channel = requests.post(
        f"{url}channel/leave/v1", json=payload_leave_channel)
    response_leave_channel_data = response_leave_channel.json()

    assert response_leave_channel.status_code == 200

    payload_leave_channel = {
        "token": response_user2_data.get('token'),
        "channel_id": response_channel_data.get('channel_id')
    }

    response_leave_channel = requests.post(
        f"{url}channel/leave/v1", json=payload_leave_channel)
    response_leave_channel_data = response_leave_channel.json()

    assert response_leave_channel_data.get('code') == 403
