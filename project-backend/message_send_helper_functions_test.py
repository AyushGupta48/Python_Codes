import pytest
import requests
from src.config import url


def send_message_many_times(message_payload, repetitions):
    i = 0
    while i < int(repetitions):
        requests.post(f"{url}message/send/v1", json=message_payload)
        i += 1


def send_dm_many_times(message_payload, repetitions):
    i = 0
    while i < int(repetitions):
        requests.post(f"{url}message/senddm/v1", json=message_payload)
        i += 1


def test_send_message(clear_data_http):
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

    message_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "message": "Hello"
    }

    send_message_many_times(message_payload, 1)

    messages_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "start": 0
    }
    response = requests.get(f"{url}channel/messages/v2",
                            params=messages_payload).json()

    assert response['messages'][0].get("message_id") == 0
    assert response['messages'][0].get("u_id") == 0
    assert response['messages'][0].get("message") == "Hello"


def test_send_dm_message(clear_data_http):
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
    requests.post(f"{url}auth/register/v2", json=payload_register2).json()

    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    message_payload = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "message": "Hello"
    }

    send_dm_many_times(message_payload, 1)

    messages_payload = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "start": 0
    }
    response = requests.get(f"{url}dm/messages/v1",
                            params=messages_payload).json()
    assert response['messages'][0].get("message_id") == 0
    assert response['messages'][0].get("u_id") == 0
    assert response['messages'][0].get("message") == "Hello"
