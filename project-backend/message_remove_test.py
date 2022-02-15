from flask.globals import request
import pytest
import requests
from src.config import url


def test_invalid_token(clear_data_http):
    message_remove_payload = {
        "token": 0,
        "message_id": 0
    }
    response_user = requests.delete(
        f"{url}message/remove/v1", json=message_remove_payload).json()

    assert response_user.get('code') == 403


def test_http_not_sent_by_user(clear_data_http):
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

    message_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "message": "Hello!"
    }
    requests.post(f"{url}message/send/v1", json=message_payload)

    message_remove_payload = {
        "token": response_register2.get('token'),
        "message_id": 0
    }
    response_user = requests.delete(
        f"{url}message/remove/v1", json=message_remove_payload).json()

    assert response_user.get('code') == 403


def test_http_not_channel_owner(clear_data_http):
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

    message_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "message": "Hello!"
    }
    requests.post(f"{url}message/send/v1", json=message_payload)

    join_payload = {
        "token": response_register2.get('token'),
        "channel_id": 0
    }
    requests.post(f"{url}channel/join/v2", json=join_payload)

    message_remove_payload = {
        "token": response_register2.get('token'),
        "message_id": 0,
    }
    response_user = requests.delete(
        f"{url}message/remove/v1", json=message_remove_payload).json()

    assert response_user.get('code') == 403


def test_http_invalid_message_id(clear_data_http):
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
        "message": "Hello!"
    }
    requests.post(f"{url}message/send/v1", json=message_payload)

    message_remove_payload = {
        "token": response_register.get('token'),
        "message_id": 900,
    }
    response_user = requests.delete(
        f"{url}message/remove/v1", json=message_remove_payload).json()

    assert response_user.get('code') == 400


def test_http_succcessful_removal(clear_data_http):
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
        "message": "Hello!"
    }
    requests.post(f"{url}message/send/v1", json=message_payload)

    message_payload2 = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "message": "This is a different message."
    }
    requests.post(f"{url}message/send/v1", json=message_payload2)

    message_remove_payload = {
        "token": response_register.get('token'),
        "message_id": 0,
    }
    requests.delete(f"{url}message/remove/v1",
                    json=message_remove_payload).json()

    message_get_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "start": 0
    }

    response_user = requests.get(
        f"{url}channel/messages/v2", params=message_get_payload).json()

    assert response_user['messages'][0].get("message_id") == 1
    assert response_user['messages'][0].get("u_id") == 0
    assert response_user['messages'][0].get(
        "message") == "This is a different message."


def test_http_no_messages_in_channel(clear_data_http):
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

    message_edit_payload = {
        "token": response_register.get('token'),
        "message_id": 0,
    }
    response = requests.delete(
        f"{url}message/remove/v1", json=message_edit_payload).json()

    assert response.get('code') == 400


def test_http_remove_in_dm(clear_data_http):
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

    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    send_dm = {
        "token": response_register2.get('token'),
        "dm_id": 0,
        "message": "Hello!"
    }
    requests.post(f"{url}message/senddm/v1", json=send_dm)

    message_remove = {
        "token": response_register2.get('token'),
        "message_id": 0,
    }
    requests.delete(f"{url}message/remove/v1", json=message_remove).json()

    messages_payload = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "start": 0
    }
    response_user = requests.get(
        f"{url}dm/messages/v1", params=messages_payload).json()

    assert response_user == {"messages": [], "start": 0, "end": -1}


def test_http_no_messages_in_dm(clear_data_http):
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

    dm_create = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=dm_create)

    message_remove_payload = {
        "token": response_register.get('token'),
        "message_id": 0
    }
    response = requests.delete(
        f"{url}message/remove/v1", json=message_remove_payload).json()

    assert response.get('code') == 400


def test_http_incorrect_message_id_in_dm(clear_data_http):
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

    dm_create = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=dm_create)

    send_dm = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "message": "Hey!"
    }
    requests.post(f"{url}message/senddm/v1", json=send_dm)

    message_remove_payload = {
        "token": response_register.get('token'),
        "message_id": 1
    }
    response = requests.delete(
        f"{url}message/remove/v1", json=message_remove_payload).json()

    assert response.get('code') == 400


def test_http_wrong_user_in_channel(clear_data_http):
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

    channel_create = {
        "token": response_register.get('token'),
        "name": "cool",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=channel_create)

    channel_join = {
        "token": response_register2.get('token'),
        "channel_id": 0
    }
    requests.post(f"{url}channel/join/v2", json=channel_join)

    send_message = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "message": "Hey"
    }
    requests.post(f"{url}message/send/v1", json=send_message)

    message_remove = {
        "token": response_register2.get('token'),
        "message_id": 0,
    }
    response = requests.delete(
        f"{url}message/remove/v1", json=message_remove).json()

    assert response.get('code') == 403


def test_http_user_not_in_DM(clear_data_http):
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

    payload_register3 = {
        "email": "valid3@gmail.com",
        "password": "abcdef",
        "name_first": "Pranav",
        "name_last": "Mangla"
    }
    response_register3 = requests.post(
        f"{url}auth/register/v2", json=payload_register3).json()

    dm_create = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=dm_create)

    send_dm = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "message": "Hiya"
    }
    requests.post(f"{url}message/senddm/v1", json=send_dm)

    message_remove = {
        "token": response_register3.get('token'),
        "message_id": 0
    }
    response = requests.delete(
        f"{url}message/remove/v1", json=message_remove).json()
        
    assert response.get('code') == 403


def test_http_member_sent_message(clear_data_http):
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

    channel_create = {
        "token": response_register.get('token'),
        "name": "yep",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=channel_create)

    channel_join = {
        "token": response_register2.get('token'),
        "channel_id": 0
    }
    requests.post(f"{url}channel/join/v2", json=channel_join)

    send_message = {
        "token": response_register2.get('token'),
        "channel_id": 0,
        "message": "Hey!"
    }
    requests.post(f"{url}message/send/v1", json=send_message)

    message_remove_payload = {
        "token": response_register2.get('token'),
        "message_id": 0
    }
    response = requests.delete(
        f"{url}message/remove/v1", json=message_remove_payload).json()
        
    assert response == {}


def test_http_wrong_user_in_dm(clear_data_http):
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

    dm_create = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=dm_create)

    send_dm = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "message": "Yep"
    }
    requests.post(f"{url}message/senddm/v1", json=send_dm)

    message_remove = {
        "token": response_register2.get('token'),
        "message_id": 0
    }
    response = requests.delete(
        f"{url}message/remove/v1", json=message_remove).json()

    assert response.get('code') == 403
