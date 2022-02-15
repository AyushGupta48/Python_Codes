import json
import pytest
import requests
from src.config import url


def send_dm_many_times(message_payload, repetitions):
    i = 0
    while i < int(repetitions):
        requests.post(f"{url}message/senddm/v1", json=message_payload)
        i += 1


def test_http_invalid_token(clear_data_http):
    messages_payload = {
        "token": 0,
        "dm_id": 0,
        "start": 0
    }
    response_user = requests.get(
        f"{url}dm/messages/v1", params=messages_payload).json()

    assert response_user.get('code') == 403


def test_http_not_part_of_dm(clear_data_http):
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

    payload_register3 = {
        "email": "valid3@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register3 = requests.post(
        f"{url}auth/register/v2", json=payload_register3).json()

    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    messages_payload = {
        "token": response_register3.get("token"),
        "dm_id": 0,
        "start": 0
    }
    response_user = requests.get(
        f"{url}dm/messages/v1", params=messages_payload).json()

    assert response_user.get('code') == 403


def test_http_invalid_dm_id(clear_data_http):
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

    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    messages_payload = {
        "token": response_register.get("token"),
        "dm_id": 900,
        "start": 0
    }
    response_user = requests.get(
        f"{url}dm/messages/v1", params=messages_payload).json()

    assert response_user.get('code') == 400


def test_http_invalid_start(clear_data_http):
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

    messages_payload = {
        "token": response_register.get("token"),
        "dm_id": 0,
        "start": 900
    }
    response_user = requests.get(
        f"{url}dm/messages/v1", params=messages_payload).json()

    assert response_user.get('code') == 400


def test_http_start_negative(clear_data_http):
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

    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    messages_payload = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "start": -6
    }
    response_user = requests.get(
        f"{url}dm/messages/v1", params=messages_payload).json()

    assert response_user.get('code') == 400


def test_http_first_case(clear_data_http):
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

    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    messages_payload = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "start": 0
    }
    response_user = requests.get(
        f"{url}dm/messages/v1", params=messages_payload).json()

    assert response_user == {"messages": [], "start": 0, "end": -1}


def test_http_one_message(clear_data_http):
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

    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    send_dm = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "message": "Hello!"
    }
    requests.post(f"{url}message/senddm/v1", json=send_dm)

    messages_payload = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "start": 0
    }
    response_user = requests.get(
        f"{url}dm/messages/v1", params=messages_payload).json()
        
    assert response_user['messages'][0].get("message_id") == 0
    assert response_user['messages'][0].get("u_id") == 0
    assert response_user['messages'][0].get("message") == "Hello!"


def test_http_fifty_dms(clear_data_http):
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

    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    message_payload = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "message": "Dingus"
    }

    send_dm_many_times(message_payload, 50)

    messages_payload = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "start": 0
    }
    response_user = requests.get(
        f"{url}dm/messages/v1", params=messages_payload).json()

    assert response_user['messages'][0].get("message_id") == 49
    assert response_user['messages'][0].get("u_id") == 0
    assert response_user['messages'][0].get("message") == "Dingus"

    assert response_user['messages'][25].get("message_id") == 24
    assert response_user['messages'][25].get("u_id") == 0
    assert response_user['messages'][25].get("message") == "Dingus"

    assert response_user['messages'][49].get("message_id") == 0
    assert response_user['messages'][49].get("u_id") == 0
    assert response_user['messages'][49].get("message") == "Dingus"

    assert response_user.get('end') == -1


def test_http_sixty_messages_not_all_returned(clear_data_http):
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

    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    message_payload = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "message": "Dingus"
    }

    send_dm_many_times(message_payload, 60)

    messages_payload = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "start": 3
    }
    response_user = requests.get(
        f"{url}dm/messages/v1", params=messages_payload).json()

    assert response_user['messages'][0].get("message_id") == 52
    assert response_user['messages'][0].get("u_id") == 0
    assert response_user['messages'][0].get("message") == "Dingus"

    assert response_user['messages'][25].get("message_id") == 27
    assert response_user['messages'][25].get("u_id") == 0
    assert response_user['messages'][25].get("message") == "Dingus"

    assert response_user['messages'][49].get("message_id") == 3
    assert response_user['messages'][49].get("u_id") == 0
    assert response_user['messages'][49].get("message") == "Dingus"

    assert response_user.get('end') == 53


def test_http_ten_messages(clear_data_http):
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

    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    message_payload = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "message": "Dingus"
    }

    send_dm_many_times(message_payload, 10)

    messages_payload = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "start": 0
    }
    response_user = requests.get(
        f"{url}dm/messages/v1", params=messages_payload).json()

    assert response_user['messages'][0].get("message_id") == 9
    assert response_user['messages'][0].get("u_id") == 0
    assert response_user['messages'][0].get("message") == "Dingus"

    assert response_user['messages'][9].get("message_id") == 0
    assert response_user['messages'][9].get("u_id") == 0
    assert response_user['messages'][9].get("message") == "Dingus"

    assert response_user.get('end') == -1
