from flask.globals import request
import pytest
import requests
from src.config import url

# Invalid token test
def test_http_invalid_token(clear_data_http):
    message_unpin_payload = {
        "token": "wrongtokena230f9h",
        "message_id": 0
    }
    response_message_unpin = requests.post(
        f"{url}message/unpin/v1", json=message_unpin_payload).json()
    
    assert response_message_unpin.get('code') == 403

# Invalid message id in a channel
def test_http_invalid_message_id_in_channel(clear_data_http):
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

    payload_create_channel2 = {
        "token": response_register.get('token'),
        "name": "2ndchannelwoo!",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel2)

    message_payload = {
        "token": response_register.get('token'),
        "channel_id": 1,
        "message": "Hello!"
    }
    requests.post(f"{url}message/send/v1", json=message_payload)    

    message_pin_payload = {
        "token": response_register.get('token'),
        "message_id": 0
    }
    requests.post(f"{url}message/pin/v1", json=message_pin_payload).json()
    
    message_unpin_payload = {
        "token": response_register.get('token'),
        "message_id": 123989
    }
    response_message_unpin = requests.post(
        f"{url}message/unpin/v1", json=message_unpin_payload).json()
    
    assert response_message_unpin.get('code') == 400

# Invalid message id in a dm
def test_http_invalid_message_id_in_dm(clear_data_http):
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

    payload_register3 = {
        "email": "valid3@gmail.com",
        "password": "abcdef",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    requests.post(f"{url}auth/register/v2", json=payload_register3).json()

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

    message_pin_payload = {
        "token": response_register.get('token'),
        "message_id": 0
    }
    requests.post(f"{url}message/pin/v1", json=message_pin_payload).json()
    
    message_unpin_payload = {
        "token": response_register.get('token'),
        "message_id": 2348928
    }
    response_message_unpin = requests.post(
        f"{url}message/unpin/v1", json=message_unpin_payload).json()
    
    assert response_message_unpin.get('code') == 400

#   Message is not pinned
def test_http_message_is_not_pinned(clear_data_http):
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

    payload_register3 = {
        "email": "valid3@gmail.com",
        "password": "abcdef",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    requests.post(f"{url}auth/register/v2", json=payload_register3).json()

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

    message_unpin_payload = {           # message unpin called here, but there was never a pinned msg
        "token": response_register.get('token'),
        "message_id": 0
    }
    response_message_unpin = requests.post(
        f"{url}message/unpin/v1", json=message_unpin_payload).json()
    
    assert response_message_unpin.get('code') == 400

# A non-owner member trying to unpin a message
def test_http_non_owner_trying_to_unpin(clear_data_http):

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

    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    payload_user2_joining_channel = {
        "token": response_register2.get('token'),
        "channel_id": 0
    }
    requests.post(f"{url}channel/join/v2", json=payload_user2_joining_channel)


    message_payload = {             # Message has been sent
        "token": response_register.get('token'),
        "channel_id": 0,
        "message": "Hello!"
    }
    requests.post(f"{url}message/send/v1", json=message_payload)    

    message_pin_payload = {         # Owner pins message
        "token": response_register.get('token'),
        "message_id": 0
    }
    requests.post(f"{url}message/pin/v1", json=message_pin_payload).json()

    message_unpin_payload = {       # Non owner tries to unpin the message
        "token": response_register2.get('token'),
        "message_id": 0
    }
    response_message_unpin = requests.post(
        f"{url}message/unpin/v1", json=message_unpin_payload).json()
    
    assert response_message_unpin.get('code') == 403

def test_http_not_in_channel(clear_data_http):
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

    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    message_payload = {             # Message has been sent
        "token": response_register.get('token'),
        "channel_id": 0,
        "message": "Hello!"
    }
    requests.post(f"{url}message/send/v1", json=message_payload)    

    message_pin_payload = {         # Owner pins a message
        "token": response_register.get('token'),
        "message_id": 0
    }
    requests.post(f"{url}message/pin/v1", json=message_pin_payload).json()

    message_unpin_payload = {       # Non member tries to unpin a message
        "token": response_register2.get('token'),
        "message_id": 0
    }
    response_message_unpin = requests.post(
        f"{url}message/unpin/v1", json=message_unpin_payload).json()
    
    assert response_message_unpin.get('code') == 400

def test_http_not_in_dm(clear_data_http):
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
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create_dm)

    send_dm = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "message": "Hello!"
    }
    requests.post(f"{url}message/senddm/v1", json=send_dm)

    message_pin_payload = {         # Owner pins a message in the dm
        "token": response_register.get('token'),
        "message_id": 0
    }
    requests.post(f"{url}message/pin/v1", json=message_pin_payload).json()

    message_unpin_payload = {       # Non member tries to unpin the message
        "token": response_register3.get('token'),
        "message_id": 0
    }
    response_message_unpin = requests.post(
        f"{url}message/unpin/v1", json=message_unpin_payload).json()
    
    assert response_message_unpin.get('code') == 400


def test_http_invalid_member_in_dm(clear_data_http):
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

    message_pin_payload = {         # Owner pins a message in the dm
        "token": response_register.get('token'),
        "message_id": 0
    }
    requests.post(f"{url}message/pin/v1", json=message_pin_payload).json()

    message_unpin_payload = {       # Non owner tries to unpin a message in the dm
        "token": response_register2.get('token'),
        "message_id": 0
    }
    response_message_unpin = requests.post(
        f"{url}message/unpin/v1", json=message_unpin_payload).json()
    
    assert response_message_unpin.get('code') == 403

# A successful message unpin in dm
def test_http_message_unpin_success_dm(clear_data_http):
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

    payload_register3 = {
        "email": "valid3@gmail.com",
        "password": "abcdef",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    requests.post(f"{url}auth/register/v2", json=payload_register3).json()

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

    message_pin_payload = {                             # Message gets pinned here
        "token": response_register.get('token'),
        "message_id": 2
    }
    requests.post(f"{url}message/pin/v1", json=message_pin_payload).json()


    message_unpin_payload = {                   # Message gets unpinned here
        "token": response_register.get('token'),
        "message_id": 2
    }
    response_message_unpin = requests.post(
        f"{url}message/unpin/v1", json=message_unpin_payload).json()
    
    assert response_message_unpin == {}


# A successful message unpin in a channel
def test_http_message_unpin_success_channel(clear_data_http):

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

    message_pin_payload = {
        "token": response_register.get('token'),
        "message_id": 0
    }
    response_message_pin = requests.post(
        f"{url}message/pin/v1", json=message_pin_payload).json()
    
    assert response_message_pin == {}

    message_unpin_payload = {
        "token": response_register.get('token'),
        "message_id": 0
    }
    response_message_unpin = requests.post(
        f"{url}message/unpin/v1", json=message_unpin_payload).json()
    
    assert response_message_unpin == {}

    # Trying to unpin again, raises input error
    message_unpin_payload = {
        "token": response_register.get('token'),
        "message_id": 0
    }
    response_message_unpin = requests.post(
        f"{url}message/unpin/v1", json=message_unpin_payload).json()
    
    assert response_message_unpin.get('code') == 400