import _pytest
import requests
from src.config import url


def test_http_invalid_token(clear_data_http):
    remove_payload = {
        "token": 0,
        "u_id": 0
    }
    response = requests.delete(
        f"{url}admin/user/remove/v1", json=remove_payload).json()

    assert response.get('code') == 403


def test_http_not_global_owner(clear_data_http):
    register1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    requests.post(f"{url}auth/register/v2", json=register1).json()

    register2 = {
        "email": "valid2@gmail.com",
        "password": "aBc293",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    register2_data = requests.post(
        f"{url}auth/register/v2", json=register2).json()

    remove_payload = {
        "token": register2_data.get('token'),
        "u_id": 0
    }
    response = requests.delete(
        f"{url}admin/user/remove/v1", json=remove_payload).json()

    assert response.get('code') == 403


def test_http_invalid_u_id(clear_data_http):
    register1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    register1_data = requests.post(
        f"{url}auth/register/v2", json=register1).json()

    remove_payload = {
        "token": register1_data.get('token'),
        "u_id": 900
    }
    response = requests.delete(
        f"{url}admin/user/remove/v1", json=remove_payload).json()

    assert response.get('code') == 400


def test_http_remove_only_owner(clear_data_http):
    register1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    register1_data = requests.post(
        f"{url}auth/register/v2", json=register1).json()

    remove_payload = {
        "token": register1_data.get('token'),
        "u_id": 0
    }
    response = requests.delete(
        f"{url}admin/user/remove/v1", json=remove_payload).json()

    assert response.get('code') == 400


def test_http_remove_another_owner(clear_data_http):
    register1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=register1).json()

    register2 = {
        "email": "valid2@gmail.com",
        "password": "aBc293",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    requests.post(f"{url}auth/register/v2", json=register2).json()

    permission = {
        "token": response_register.get('token'),
        "u_id": 1,
        "permission_id": 1
    }
    requests.post(f"{url}admin/userpermission/change/v1", json=permission)

    remove_payload = {
        "token": response_register.get('token'),
        "u_id": 1
    }
    requests.delete(f"{url}admin/user/remove/v1", json=remove_payload).json()

    response = requests.get(
        f"{url}user/profile/v1",
        params={"token": response_register.get('token'), "u_id": "1"}).json()

    assert response ==\
        {"u_id": 1,
         "email": "",
         "name_first": "Removed",
         "name_last": "user",
         "handle_str": ""}


def test_http_remove_from_channel_and_dm(clear_data_http):
    register1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=register1).json()

    register2 = {
        "email": "valid2@gmail.com",
        "password": "aBc293",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register2 = requests.post(
        f"{url}auth/register/v2", json=register2).json()

    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    payload_join = {
        "token": response_register2.get('token'),
        "channel_id": 0
    }
    requests.post(f"{url}channel/join/v2", json=payload_join)

    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    remove_payload = {
        "token": response_register.get('token'),
        "u_id": 1
    }
    requests.delete(f"{url}admin/user/remove/v1", json=remove_payload).json()

    channel_details_payload = {
        "token": response_register.get('token'),
        "channel_id": 0
    }
    channel_response = requests.get(
        f"{url}channel/details/v2", params=channel_details_payload).json()

    assert channel_response.get('all_members') == [
                                {'u_id': 0,
                                    "email": "valid@gmail.com",
                                    "name_first": "Daniel",
                                    "name_last": "Li",
                                    "handle_str": "danielli"}]

    dm_details_payload = {
        "token": response_register.get('token'),
        "dm_id": 0
    }
    dm_response = requests.get(
        f"{url}dm/details/v1", params=dm_details_payload).json()

    assert dm_response.get('members') == [
                                {'u_id': 0,
                                    "email": "valid@gmail.com",
                                    "name_first": "Daniel",
                                    "name_last": "Li",
                                    "handle_str": "danielli"}]


def test_http_remove_from_channel_and_dm_and_messages(clear_data_http):
    register1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=register1).json()

    register2 = {
        "email": "valid2@gmail.com",
        "password": "aBc293",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register2 = requests.post(
        f"{url}auth/register/v2", json=register2).json()

    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    payload_join = {
        "token": response_register2.get('token'),
        "channel_id": 0
    }
    requests.post(f"{url}channel/join/v2", json=payload_join)

    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    message_payload = {
        "token": response_register2.get('token'),
        "dm_id": 0,
        "message": "Hello!"
    }
    requests.post(f"{url}message/senddm/v1", json=message_payload)

    message_send = {
        "token": response_register2.get('token'),
        "channel_id": 0,
        "message": "YEET"
    }
    requests.post(f"{url}message/send/v1", json=message_send)

    remove_payload = {
        "token": response_register.get('token'),
        "u_id": 1
    }
    response_removed = requests.delete(
        f"{url}admin/user/remove/v1", json=remove_payload).json()

    assert response_removed == {}

    channel_details_payload = {
        "token": response_register.get('token'),
        "channel_id": 0
    }
    channel_response = requests.get(
        f"{url}channel/details/v2", params=channel_details_payload).json()

    assert channel_response.get('all_members') == [
                                {'u_id': 0,
                                    "email": "valid@gmail.com",
                                    "name_first": "Daniel",
                                    "name_last": "Li",
                                    "handle_str": "danielli"}]

    dm_details_payload = {
        "token": response_register.get('token'),
        "dm_id": 0
    }
    dm_response = requests.get(
        f"{url}dm/details/v1", params=dm_details_payload).json()

    assert dm_response.get('members') == [
                                {'u_id': 0,
                                    "email": "valid@gmail.com",
                                    "name_first": "Daniel",
                                    "name_last": "Li",
                                    "handle_str": "danielli"}]

    messages_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "start": 0
    }
    response_messages = requests.get(
        f"{url}channel/messages/v2", params=messages_payload).json()

    assert response_messages['messages'][0].get("message_id") == 1
    assert response_messages['messages'][0].get("u_id") == 1
    assert response_messages['messages'][0].get("message") == "Removed user"

    dm_messages = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "start": 0
    }
    response_dm = requests.get(
        f"{url}dm/messages/v1", params=dm_messages).json()

    print(response_dm)
    assert response_dm['messages'][0].get("message_id") == 0
    assert response_dm['messages'][0].get("u_id") == 1
    assert response_dm['messages'][0].get("message") == "Removed user"


def test_http_remove_from_channel_and_dm_and_messages_multiple(clear_data_http):
    register1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=register1).json()

    register3 = {
        "email": "valid3@gmail.com",
        "password": "aBc293",
        "name_first": "Pranav",
        "name_last": "Mangla"
    }
    requests.post(f"{url}auth/register/v2", json=register3).json()

    register2 = {
        "email": "valid2@gmail.com",
        "password": "aBc293",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register2 = requests.post(
        f"{url}auth/register/v2", json=register2).json()

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

    payload_join = {
        "token": response_register2.get('token'),
        "channel_id": 0
    }
    requests.post(f"{url}channel/join/v2", json=payload_join)

    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [2]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    message_payload = {
        "token": response_register2.get('token'),
        "dm_id": 0,
        "message": "Hello!"
    }
    requests.post(f"{url}message/senddm/v1", json=message_payload)

    message_send = {
        "token": response_register2.get('token'),
        "channel_id": 0,
        "message": "YEET"
    }
    requests.post(f"{url}message/send/v1", json=message_send)

    remove_payload = {
        "token": response_register.get('token'),
        "u_id": 1
    }
    response_removed = requests.delete(
        f"{url}admin/user/remove/v1", json=remove_payload).json()

    assert response_removed == {}

    channel_details_payload = {
        "token": response_register.get('token'),
        "channel_id": 0
    }
    channel_response = requests.get(
        f"{url}channel/details/v2", params=channel_details_payload).json()

    assert channel_response.get('all_members') == [
                                {'u_id': 0,
                                    "email": "valid@gmail.com",
                                    "name_first": "Daniel",
                                    "name_last": "Li",
                                    "handle_str": "danielli"},
                                    {'u_id': 2,
                                     "email": "valid2@gmail.com",
                                     "name_first": "Vikram",
                                     "name_last": "Sundar",
                                     "handle_str": "vikramsundar"}]

    dm_details_payload = {
        "token": response_register.get('token'),
        "dm_id": 0
    }
    dm_response = requests.get(
        f"{url}dm/details/v1", params=dm_details_payload).json()

    assert dm_response.get('members') == [
                                {'u_id': 0,
                                    "email": "valid@gmail.com",
                                    "name_first": "Daniel",
                                    "name_last": "Li",
                                    "handle_str": "danielli"},
                                    {'u_id': 2,
                                     "email": "valid2@gmail.com",
                                     "name_first": "Vikram",
                                     "name_last": "Sundar",
                                     "handle_str": "vikramsundar"}]

    messages_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "start": 0
    }
    response_messages = requests.get(
        f"{url}channel/messages/v2", params=messages_payload).json()

    assert response_messages['messages'][0].get("message_id") == 1
    assert response_messages['messages'][0].get("u_id") == 2
    assert response_messages['messages'][0].get("message") == "YEET"

    dm_messages = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "start": 0
    }
    response_dm = requests.get(
        f"{url}dm/messages/v1", params=dm_messages).json()
        
    assert response_dm['messages'][0].get("message_id") == 0
    assert response_dm['messages'][0].get("u_id") == 2
    assert response_dm['messages'][0].get("message") == "Hello!"
