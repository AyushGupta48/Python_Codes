from flask.globals import request
import pytest
import requests
from src.config import url


# Invalid token passed in (Access Error)
def test_http_invalid_token(clear_data_http):
    message_unreact_payload = {
        "token": "wrongtoken",
        "message_id": 0,
        "react_id": 1
    }
    response_message_unreact = requests.post(
        f"{url}message/unreact/v1", json=message_unreact_payload).json()

    assert response_message_unreact.get('code') == 403

# A invalid message id is passed in (Input Error)
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

    message_react_payload = {
        "token": response_register.get('token'),
        "message_id": 0,
        "react_id": 1
    }
    requests.post(f"{url}message/react/v1", json=message_react_payload).json()

    message_unreact_payload = {
        "token": response_register.get('token'),
        "message_id": 123894,
        "react_id": 1
    }
    response_message_unreact = requests.post(
        f"{url}message/unreact/v1", json=message_unreact_payload).json()
    
    assert response_message_unreact.get('code') == 400

# A react id that is not 1 is passed in (Input Error)
def test_http_invalid_react_id(clear_data_http):
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

    
    message_react_payload = {
        "token": response_register.get('token'),
        "message_id": 0,
        "react_id": 1
    }
    requests.post(f"{url}message/react/v1", json=message_react_payload).json()

    message_unreact_payload = {
        "token": response_register.get('token'),
        "message_id": 0,
        "react_id": 234
    }
    response_message_unreact = requests.post(
        f"{url}message/unreact/v1", json=message_unreact_payload).json()    
    
    assert response_message_unreact.get('code') == 400


# Message does not contain a react (Input Error)

def test_http_duplicate_message_react(clear_data_http):
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

    
    message_unreact_payload = {
        "token": response_register.get('token'),
        "message_id": 0,
        "react_id": 1
    }
    response_message_unreact = requests.post(
        f"{url}message/unreact/v1", json=message_unreact_payload).json()


    assert response_message_unreact.get('code') == 400

# Trying to unreact to a message that the auth user is not part of (Access Error)
def test_http_not_a_member(clear_data_http):
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

    payload_user2_joining_channel = {
        "token": response_register2.get('token'),
        "channel_id": 0
    }

    requests.post(f"{url}channel/join/v2", json=payload_user2_joining_channel)   
    
    message_react_payload = {
        "token": response_register2.get('token'),
        "message_id": 0,
        "react_id": 1
    }        
    
    requests.post(f"{url}message/react/v1", json=message_react_payload).json()

    payload_leave_channel = {
        "token": response_register2.get('token'),
        "channel_id": 0
    }

    requests.post(f"{url}channel/leave/v1", json=payload_leave_channel)   

    message_unreact_payload = {
        "token": response_register2.get('token'),
        "message_id": 0,
        "react_id": 1
    }        
    
    response_message_unreact = requests.post(
        f"{url}message/unreact/v1", json=message_unreact_payload).json()

    assert response_message_unreact.get('code') == 400

# Trying to unreact to a message in a dm that the auth user is not part of (Access Error)
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
        "name_first": "Pranav",
        "name_last": "Mangla"
    }
    response_register2 = requests.post(
        f"{url}auth/register/v2", json=payload_register2).json()

    payload_register3 = {
        "email": "valid3@gmail.com",
        "password": "abcdef",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_register3 = requests.post(
        f"{url}auth/register/v2", json=payload_register3).json()
    
    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [1,2]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    send_dm = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "message": "Hello!"
    }
    requests.post(f"{url}message/senddm/v1", json=send_dm)


    message_react_successful = {
        "token": response_register3.get('token'),
        "message_id": 0,
        "react_id": 1
    }
    requests.post(
        f"{url}message/react/v1", json=message_react_successful).json()

    message_react_by_user2 = {
        "token": response_register2.get('token'),
        "message_id": 0,
        "react_id": 1
    }
    requests.post(f"{url}message/react/v1", json=message_react_by_user2).json()    

    leave_payload = {
        "token": response_register2.get("token"),
        "dm_id": 0
    }
    requests.post(f"{url}dm/leave/v1", json=leave_payload).json()    

    message_unreact_payload = {
        "token": response_register2.get('token'),
        "message_id": 0,
        "react_id": 1
    }        
    
    response_message_unreact = requests.post(
        f"{url}message/unreact/v1", json=message_unreact_payload).json()

    assert response_message_unreact.get('code') == 400

# Reacting to only 1 message in a dm that that has multiple messages
def test_http_multiple_messages(clear_data_http):
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

    payload_create_dm2 = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm2)

    payload_create_dm3 = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm3)


    send_dm = {
        "token": response_register.get('token'),
        "dm_id": 1,
        "message": "Hello!"
    }
    requests.post(f"{url}message/senddm/v1", json=send_dm)

    send_dm2 = {
        "token": response_register.get('token'),
        "dm_id": 2,
        "message": "World"
    }
    requests.post(f"{url}message/senddm/v1", json=send_dm2)

    send_dm3 = {
        "token": response_register.get('token'),
        "dm_id": 2,
        "message": "dontbreak"
    }
    requests.post(f"{url}message/senddm/v1", json=send_dm3)

    message_react_successful = {
        "token": response_register.get('token'),
        "message_id": 2,
        "react_id": 1
    }
    requests.post(f"{url}message/react/v1", json=message_react_successful).json()

    message_unreact_successful = {
        "token": response_register.get('token'),
        "message_id": 2,
        "react_id": 1        
    }
    response_successful_unreact = requests.post(
        f"{url}message/unreact/v1", json=message_unreact_successful).json()
    
    assert response_successful_unreact == {}

def test_http_simple_channel_unreact(clear_data_http):

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

    message_react_payload = {
        "token": response_register.get('token'),
        "message_id": 0,
        "react_id": 1
    }
    requests.post(f"{url}message/react/v1", json=message_react_payload).json()

    message_unreact_payload = {
        "token": response_register.get('token'),
        "message_id": 0,
        "react_id": 1
    }
    response_message_unreact = requests.post(
        f"{url}message/unreact/v1", json=message_unreact_payload).json()
    
    assert response_message_unreact == {}
        