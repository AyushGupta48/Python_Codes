import pytest
import requests
from src.config import url

def test_invalid_token(clear_data_http):
    message_payload = {
        "token": 0,
        "og_message_id": 0,
        "message": "Hello!",
        "channel_id": 0,
        "dm_id": -1
    }
    response_user = requests.post(
        f"{url}message/share/v1", json=message_payload).json()

    assert response_user.get('code') == 403

def test_both_channel_id_and_dm_id_positive(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    message_payload = {
        "token": response_register.get('token'),
        "og_message_id": 0,
        "message": "Hello!",
        "channel_id": 0,
        "dm_id": 0
    }

    response_user = requests.post(
        f"{url}message/share/v1", json=message_payload).json()
    
    assert response_user.get('code') == 400

def test_both_channel_id_and_dm_id_negative(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    message_payload = {
        "token": response_register.get('token'),
        "og_message_id": 0,
        "message": "Hello!",
        "channel_id": -1,
        "dm_id": -1
    }

    response_user = requests.post(
        f"{url}message/share/v1", json=message_payload).json()
    
    assert response_user.get('code') == 400

def test_invalid_channel_invalid_dm(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    message_payload = {
        "token": response_register.get('token'),
        "og_message_id": 0,
        "message": "Hello!",
        "channel_id": -1,
        "dm_id": 1
    }
    response_user = requests.post(
        f"{url}message/share/v1", json=message_payload).json()
        
    assert response_user.get('code') == 400

    message_payload = {
        "token": response_register.get('token'),
        "og_message_id": 0,
        "message": "Hello!",
        "channel_id": 1,
        "dm_id": -1
    }
    response_user = requests.post(
        f"{url}message/share/v1", json=message_payload).json()

    assert response_user.get('code') == 400

def test_dm_permissions(clear_data_http):
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
    
    payload_register3 = {
        "email": "valid3@gmail.com",
        "password": "abcdef",
        "name_first": "asdfasdf",
        "name_last": "Sunasdfasddar"
    }
    response_register3 = requests.post(
        f"{url}auth/register/v2", json=payload_register3).json()

    message_payload = {
        "token": response_register3.get('token'),
        "og_message_id": 0,
        "message": "Hello!",
        "channel_id": -1,
        "dm_id": 0
    }
    response_user = requests.post(
        f"{url}message/share/v1", json=message_payload).json()
        
    assert response_user.get('code') == 403

def test_channel_permissions(clear_data_http):
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

    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    payload_register3 = {
        "email": "valid3@gmail.com",
        "password": "abcdef",
        "name_first": "asdfasdf",
        "name_last": "Sunasdfasddar"
    }
    response_register3 = requests.post(
        f"{url}auth/register/v2", json=payload_register3).json()

    message_payload = {
        "token": response_register3.get('token'),
        "og_message_id": 0,
        "message": "Hello!",
        "channel_id": 0,
        "dm_id": -1
    }
    response_user = requests.post(
        f"{url}message/share/v1", json=message_payload).json()
        
    assert response_user.get('code') == 403


def test_share_message_too_long(clear_data_http):
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
        "og_message_id": 0,
        "message": "Lorem ipsudasfnladnm dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. N",
        "channel_id": -1,
        "dm_id": 1
    }
    response_user = requests.post(
        f"{url}message/share/v1", json=message_payload).json()
        
    assert response_user.get('code') == 400