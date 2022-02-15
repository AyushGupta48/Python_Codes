import pytest
import requests
import time
from src.config import url

def test_invalid_token(clear_data_http):
    message_payload = {
        "token": 0,
        "channel_id": 0,
        "message": "Hello!",
        "time_sent": time.time()
    }
    response_user = requests.post(
        f"{url}message/sendlater/v1", json=message_payload).json()

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

    message_payload = {
        "token": response_register2.get('token'),
        "channel_id": 0,
        "message": "Hello!",
        "time_sent": time.time()
    }

    response_user = requests.post(
        f"{url}message/sendlater/v1", json=message_payload).json()

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

    message_payload = {
        "token": response_register.get('token'),
        "channel_id": 900,
        "message": "Hello!",
        "time_sent": time.time()
    }
    response_user = requests.post(
        f"{url}message/sendlater/v1", json=message_payload).json()

    assert response_user.get('code') == 400

def test_http_empty_message(clear_data_http):
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
        "message": "",
        "time_sent": time.time()
    }
    response_user = requests.post(
        f"{url}message/sendlater/v1", json=message_payload).json()

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
        "message": "Lorem ipsudasfnladnm dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. N",
        "time_sent": time.time()
    }
    response_user = requests.post(
        f"{url}message/sendlater/v1", json=message_payload).json()
        
    assert response_user.get('code') == 400

def test_http_time_sent_past(clear_data_http):
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
        "message": "Dingus",
        "time_sent": time.time() - 50
    }
    response_user = requests.post(
        f"{url}message/sendlater/v1", json=message_payload).json()

    assert response_user.get('code') == 400

def test_successful_send_later(clear_data_http):
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
        "message": "Dingus",
        "time_sent": time.time() + 3
    }
    requests.post(f"{url}message/sendlater/v1", json=message_payload).json()  

    messages_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "start": 0
    }
    response_user = requests.get(f"{url}channel/messages/v2", params=messages_payload).json()

    assert response_user == {"messages": [], "start": 0, "end": -1}

    time.sleep(4)

    messages_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "start": 0
    }
    response_user = requests.get(f"{url}channel/messages/v2", params=messages_payload).json()

    assert response_user['messages'][0].get("message_id") == 0
    assert response_user['messages'][0].get("u_id") == 0
    assert response_user['messages'][0].get("message") == "Dingus"