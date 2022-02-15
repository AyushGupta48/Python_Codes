import pytest
import requests
from src.config import url
import time

def test_invalid_token(clear_data_http):
    standup_payload = {
        "token": 0,
        "channel_id": 0,
        "length": 3
    }
    response_user = requests.post(
        f"{url}standup/start/v1", json=standup_payload).json()

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
        "length": 3
    }

    response_user = requests.post(
        f"{url}standup/start/v1", json=standup_payload).json()

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
        "length": 3
    }
    response_user = requests.post(
        f"{url}standup/start/v1", json=standup_payload).json()

    assert response_user.get('code') == 400

def test_http_invalid_length(clear_data_http):
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
        "length": "dingus"
    }
    response_user = requests.post(
        f"{url}standup/start/v1", json=standup_payload).json()

    assert response_user.get('code') == 400

    standup_payload2 = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "length": -7
    }
    response_user = requests.post(
        f"{url}standup/start/v1", json=standup_payload2).json()
    
    assert response_user.get('code') == 400

def test_http_standup_already_active(clear_data_http):
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
        "length": 4
    }
    response_user2 = requests.post(
        f"{url}standup/start/v1", json=standup_payload2).json()
    
    assert response_user2.get('code') == 400

def test_http_time_finish_correct(clear_data_http):
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

    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    standup_payload = {
        "token": response_register.get('token'),
        "channel_id": 1,
        "length": 3
    }
    response_user = requests.post(f"{url}standup/start/v1", json=standup_payload).json()

    assert response_user.get('time_finish') == int((time.time() + 3))

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

    standup_payload = {
        "token": response_register.get('token'),
        "channel_id": 1,
    }
    response_user = requests.get(
        f"{url}standup/active/v1", params=standup_payload).json()

    assert response_user == {
        'is_active': True,
        'time_finish': int(time.time()) + 3
    }

    standup_send = {
        "token": response_register.get('token'),
        "channel_id": 1,
        "message": "I am a dog, moo!"
    }
    requests.post(f"{url}standup/send/v1", json=standup_send).json

    standup_send = {
        "token": response_register.get('token'),
        "channel_id": 1,
        "message": "Yep"
    }
    requests.post(f"{url}standup/send/v1", json=standup_send).json

    messages_payload = {
        "token": response_register.get("token"),
        "channel_id": 0,
        "start": 0
    }
    response_user = requests.get(f"{url}channel/messages/v2", params=messages_payload).json()
    assert response_user == {"messages": [], "start": 0, "end": -1}

    time.sleep(4)

    messages_payload = {
        "token": response_register.get("token"),
        "channel_id": 1,
        "start": 0
    }
    response_user = requests.get(f"{url}channel/messages/v2", params=messages_payload).json()

    assert response_user['messages'][0].get("message_id") == 0
    assert response_user['messages'][0].get("u_id") == 0
    assert response_user['messages'][0].get("message") == "vikramsundar: I am a dog, moo!\nvikramsundar: Yep"


