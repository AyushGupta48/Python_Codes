from flask.globals import request
import pytest
import requests
from src.config import url

# Invalid token test
def test_http_invalid_token(clear_data_http):
    message_pin_payload = {
        "token": "wrongtokena230f9h",
        "message_id": 0
    }
    response_message_pin = requests.post(
        f"{url}message/pin/v1", json=message_pin_payload).json()
    
    assert response_message_pin.get('code') == 403

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
        "message_id": 234789
    }
    response_message_pin = requests.post(
        f"{url}message/pin/v1", json=message_pin_payload).json()
    
    assert response_message_pin.get('code') == 400

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
        "message_id": 234789
    }
    response_message_pin = requests.post(
        f"{url}message/pin/v1", json=message_pin_payload).json()
    
    assert response_message_pin.get('code') == 400

#   Message already pinned
def test_http_message_already_pinned(clear_data_http):
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
    
    message_pin_again_payload = {                       # Message tries to get pinned again
        "token": response_register.get('token'),
        "message_id": 2
    }
    response_message_pin_again = requests.post(
        f"{url}message/pin/v1", json=message_pin_again_payload).json()
            
    
    assert response_message_pin_again.get('code') == 400
    # assert response_message_pin_again == {}

# A non-owner member trying to pin a message
def test_http_non_owner_trying_to_pin(clear_data_http):

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

    message_pin_payload = {         # Non owner tries to pin a message to the channel
        "token": response_register2.get('token'),
        "message_id": 0
    }
    response_message_pin = requests.post(
        f"{url}message/pin/v1", json=message_pin_payload).json()
    
    assert response_message_pin.get('code') == 403

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

    message_pin_payload = {         # Non member tries to pin a message
        "token": response_register2.get('token'),
        "message_id": 0
    }
    response_message_pin = requests.post(
        f"{url}message/pin/v1", json=message_pin_payload).json()

    assert response_message_pin.get('code') == 400

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

    message_pin_payload = {         # Non member tries to pin a message in the dm
        "token": response_register3.get('token'),
        "message_id": 0
    }
    response_message_pin = requests.post(
        f"{url}message/pin/v1", json=message_pin_payload).json()

    assert response_message_pin.get('code') == 400



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

    message_pin_payload = {         # Non owner tries to pin a message in the dm
        "token": response_register2.get('token'),
        "message_id": 0
    }
    response_message_pin = requests.post(
        f"{url}message/pin/v1", json=message_pin_payload).json()

    assert response_message_pin.get('code') == 403

# A successful message pin in dm
def test_http_message_pin_success_dm(clear_data_http):
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
    response_message_pin = requests.post(
        f"{url}message/pin/v1", json=message_pin_payload).json()
       
    assert response_message_pin == {}

# A successful message pin in a channel
def test_http_message_pin_success_channel(clear_data_http):

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

    message_pin_payload = {
        "token": response_register.get('token'),
        "message_id": 0
    }
    response_message_pin = requests.post(
        f"{url}message/pin/v1", json=message_pin_payload).json()  

    assert response_message_pin.get('code') == 400  