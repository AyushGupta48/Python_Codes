from flask.globals import request
import pytest
import requests
from src.config import url


def test_invalid_token(clear_data_http):
    message_edit_payload = {
        "token": 0,
        "message_id": 0,
        "message": "Hello!"
    }
    response_user = requests.put(
        f"{url}message/edit/v1", json=message_edit_payload).json()

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

    message_edit_payload = {
        "token": response_register2.get('token'),
        "message_id": 0,
        "message": "Changed the message"
    }
    response_user = requests.put(
        f"{url}message/edit/v1", json=message_edit_payload).json()

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

    message_edit_payload = {
        "token": response_register2.get('token'),
        "message_id": 0,
        "message": "Changed the message"
    }
    response_user = requests.put(
        f"{url}message/edit/v1", json=message_edit_payload).json()

    assert response_user.get('code') == 403

# Message length > 1000


def test_http_message_too_long(clear_data_http):
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

    message_edit_payload = {
        "token": response_register.get('token'),
        "message_id": 0,
        "message": "Lorem ipsudasfnladnm dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. N"
    }
    response_user = requests.put(
        f"{url}message/edit/v1", json=message_edit_payload).json()

    assert response_user.get('code') == 400


def test_http_invalid_message_id(clear_data_http):
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

    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [1],
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    send_dm = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "message": "Hello!"
    }
    requests.post(f"{url}message/senddm/v1", json=send_dm)

    message_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "message": "Hello!"
    }
    requests.post(f"{url}message/send/v1", json=message_payload)

    message_edit_payload = {
        "token": response_register.get('token'),
        "message_id": 900,
        "message": "This has been changed."
    }
    response_user = requests.put(
        f"{url}message/edit/v1", json=message_edit_payload).json()
        
    assert response_user.get('code') == 400


def test_http_successful_message_edit(clear_data_http):
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

    message_edit_payload = {
        "token": response_register.get('token'),
        "message_id": 0,
        "message": "This message has been successfully changed."
    }
    requests.put(f"{url}message/edit/v1", json=message_edit_payload).json()

    message_get_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "start": 0
    }

    response_user = requests.get(
        f"{url}channel/messages/v2", params=message_get_payload).json()

    assert response_user['messages'][0].get("message_id") == 0
    assert response_user['messages'][0].get("u_id") == 0
    assert response_user['messages'][0].get(
        "message") == "This message has been successfully changed."


def test_http_delete_message(clear_data_http):
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

    message_edit_payload = {
        "token": response_register.get('token'),
        "message_id": 0,
        "message": ""
    }
    requests.put(f"{url}message/edit/v1", json=message_edit_payload).json()

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
        "message": "yeet"
    }
    response = requests.put(f"{url}message/edit/v1",
                            json=message_edit_payload).json()
    assert response.get('code') == 400


def test_http_message_in_DM(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    payload_register2 = {
        "email": "valid@2gmail.com",
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

    payload_create_dm2 = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm2)

    message_payload = {
        "token": response_register.get('token'),
        "dm_id": 1,
        "message": "Hello!"
    }
    requests.post(f"{url}message/senddm/v1", json=message_payload).json()

    message_edit_payload = {
        "token": response_register.get('token'),
        "message_id": 0,
        "message": "yeet"
    }
    requests.put(f"{url}message/edit/v1", json=message_edit_payload).json()

    messages_payload = {
        "token": response_register.get('token'),
        "dm_id": 1,
        "start": 0
    }
    response = requests.get(f"{url}dm/messages/v1",
                            params=messages_payload).json()
    assert response['messages'][0].get("message_id") == 0
    assert response['messages'][0].get("u_id") == 0
    assert response['messages'][0].get("message") == "yeet"


def test_http_user_doesnt_have_permission_to_edit_channel(clear_data_http):
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

    payload_join = {
        "token": response_register2.get('token'),
        "channel_id": 0
    }
    requests.post(f"{url}channel/join/v2", json=payload_join).json()

    send_payload = {
        "token": response_register.get("token"),
        "channel_id": 0,
        "message": "Dingus"
    }
    requests.post(f"{url}message/send/v1", json=send_payload)

    message_edit_payload = {
        "token": response_register2.get('token'),
        "message_id": 0,
        "message": "yeet"
    }
    response = requests.put(f"{url}message/edit/v1",
                            json=message_edit_payload).json()
    assert response.get('code') == 403


def test_http_user_has_permission_to_edit_channel(clear_data_http):
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

    payload_join = {
        "token": response_register2.get('token'),
        "channel_id": 0
    }
    requests.post(f"{url}channel/join/v2", json=payload_join).json()

    send_payload = {
        "token": response_register2.get("token"),
        "channel_id": 0,
        "message": "Dingus"
    }
    requests.post(f"{url}message/send/v1", json=send_payload)

    message_edit_payload = {
        "token": response_register2.get('token'),
        "message_id": 0,
        "message": "yeet"
    }
    response = requests.put(f"{url}message/edit/v1",
                            json=message_edit_payload).json()
    assert response == {}


def test_http_user_not_in_dm(clear_data_http):
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

    message_edit = {
        "token": response_register3.get('token'),
        "message_id": 0,
        "message": "yeet"
    }
    response = requests.put(f"{url}message/edit/v1", json=message_edit).json()
    assert response.get('code') == 403


def test_http_user_didnt_send_message(clear_data_http):
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
        "token": response_register.get('token'),
        "dm_id": 0,
        "message": "Hello!"
    }
    requests.post(f"{url}message/senddm/v1", json=send_dm)

    message_edit = {
        "token": response_register2.get('token'),
        "message_id": 0,
        "message": "yeet"
    }
    response = requests.put(f"{url}message/edit/v1", json=message_edit).json()
    assert response.get('code') == 403


def test_http_delete_in_dm(clear_data_http):
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

    message_edit = {
        "token": response_register2.get('token'),
        "message_id": 0,
        "message": ""
    }
    requests.put(f"{url}message/edit/v1", json=message_edit).json()

    messages_payload = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "start": 0
    }
    response_user = requests.get(
        f"{url}dm/messages/v1", params=messages_payload).json()
    assert response_user == {"messages": [], "start": 0, "end": -1}
