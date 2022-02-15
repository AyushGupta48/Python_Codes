import pytest
import requests
from src.config import url
import time

def test_invalid_token(clear_data_http):
    standup_payload = {
        "token": 0,
        "channel_id": 0,
        "message": "yeet"
    }
    response_user = requests.post(
        f"{url}standup/send/v1", json=standup_payload).json()

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
        "message": "yeet"
    }

    response_user = requests.post(
        f"{url}standup/send/v1", json=standup_payload).json()

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
        "message": "yeet"
    }
    response_user = requests.post(
        f"{url}standup/send/v1", json=standup_payload).json()

    assert response_user.get('code') == 400

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
        "message": "Lorem ipsudasfnladnm dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. N"
    }
    response_user = requests.post(
        f"{url}standup/send/v1", json=message_payload).json()
        
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
        "message": "hey"
    }
    response_user = requests.post(
        f"{url}standup/send/v1", json=standup_payload).json()

    assert response_user.get('code') == 400

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
        "length": 3
    }
    requests.post(f"{url}standup/start/v1", json=standup_payload).json()

    standup_send = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "message": "I am a dog, moo!"
    }
    requests.post(f"{url}standup/send/v1", json=standup_send).json

    standup_send = {
        "token": response_register.get('token'),
        "channel_id": 0,
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
        "channel_id": 0,
        "start": 0
    }
    response_user = requests.get(f"{url}channel/messages/v2", params=messages_payload).json()

    assert response_user['messages'][0].get("message_id") == 0
    assert response_user['messages'][0].get("u_id") == 0
    assert response_user['messages'][0].get("message") == "vikramsundar: I am a dog, moo!\nvikramsundar: Yep"
