import pytest
import requests
from src.config import url


def test_http_invalid_token(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_user_2 = {
        "email": "valid2@gmail.com",
        "password": "alkdjnfklasd",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_user2 = requests.post(
        f"{url}auth/register/v2", json=payload_user_2)
    response_user2_data = response_user2.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    payload_user2_joining_channel = {
        "token": response_user2_data.get('token'),
        "channel_id": response_channel_data.get('channel_id')
    }

    requests.post(f"{url}channel/join/v2", json=payload_user2_joining_channel)

    payload_addowner_channel = {
        "token": response_user_data.get('token'),
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": response_user2_data.get('auth_user_id')  # U Id 1
    }

    requests.post(f"{url}channel/addowner/v1", json=payload_addowner_channel)

    payload_removeowner = {
        "token": "invalidtoken",
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": response_user2_data.get('auth_user_id')  # U Id 1
    }

    response_removeowner = requests.post(
        f"{url}channel/removeowner/v1", json=payload_removeowner)
    response_removeowner_data = response_removeowner.json()

    assert response_removeowner_data.get('code') == 403


def test_http_already_member(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_user_2 = {
        "email": "valid2@gmail.com",
        "password": "alkdjnfklasd",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_user2 = requests.post(
        f"{url}auth/register/v2", json=payload_user_2)
    response_user2_data = response_user2.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    payload_user2_joining_channel = {
        "token": response_user2_data.get('token'),
        "channel_id": response_channel_data.get('channel_id')
    }

    requests.post(f"{url}channel/join/v2", json=payload_user2_joining_channel)

    payload_addowner_channel = {
        "token": response_user_data.get('token'),
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": response_user2_data.get('auth_user_id')  # U Id 1
    }

    requests.post(f"{url}channel/addowner/v1", json=payload_addowner_channel)

    payload_removeowner = {
        "token": response_user_data.get('token'),
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": response_user2_data.get('auth_user_id')  # U Id 1
    }

    response_removeowner = requests.post(
        f"{url}channel/removeowner/v1", json=payload_removeowner)
    response_removeowner_data = response_removeowner.json()

    assert response_removeowner.status_code == 200

    payload_removeowner = {
        "token": response_user_data.get('token'),
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": response_user2_data.get('auth_user_id')  # U Id 1
    }

    response_removeowner = requests.post(
        f"{url}channel/removeowner/v1", json=payload_removeowner)
    response_removeowner_data = response_removeowner.json()

    assert response_removeowner_data.get('code') == 400


def test_http_invalid_channel_id(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_user_2 = {
        "email": "valid2@gmail.com",
        "password": "alkdjnfklasd",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_user2 = requests.post(
        f"{url}auth/register/v2", json=payload_user_2)
    response_user2_data = response_user2.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    payload_user2_joining_channel = {
        "token": response_user2_data.get('token'),
        "channel_id": response_channel_data.get('channel_id')
    }

    requests.post(f"{url}channel/join/v2", json=payload_user2_joining_channel)

    payload_addowner_channel = {
        "token": response_user_data.get('token'),
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": response_user2_data.get('auth_user_id')  # U Id 1
    }

    requests.post(f"{url}channel/addowner/v1", json=payload_addowner_channel)

    payload_removeowner = {
        "token": response_user_data.get('token'),
        "channel_id": 23874,  # Wrong channel id
        "u_id": response_user2_data.get('auth_user_id')  # U Id 1
    }

    response_removeowner = requests.post(
        f"{url}channel/removeowner/v1", json=payload_removeowner)
    response_removeowner_data = response_removeowner.json()

    assert response_removeowner_data.get('code') == 400


def test_http_invalid_user_id(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_user_2 = {
        "email": "valid2@gmail.com",
        "password": "alkdjnfklasd",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_user2 = requests.post(
        f"{url}auth/register/v2", json=payload_user_2)
    response_user2_data = response_user2.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    payload_user2_joining_channel = {
        "token": response_user2_data.get('token'),
        "channel_id": response_channel_data.get('channel_id')
    }

    requests.post(f"{url}channel/join/v2", json=payload_user2_joining_channel)

    payload_addowner_channel = {
        "token": response_user_data.get('token'),
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": response_user2_data.get('auth_user_id')  # U Id 1
    }

    requests.post(f"{url}channel/addowner/v1", json=payload_addowner_channel)

    payload_removeowner = {
        "token": response_user_data.get('token'),
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": 12893  # Wrong user id
    }

    response_removeowner = requests.post(
        f"{url}channel/removeowner/v1", json=payload_removeowner)
    response_removeowner_data = response_removeowner.json()

    assert response_removeowner_data.get('code') == 400


def test_http_user_not_member_of_channel(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_user_2 = {
        "email": "valid2@gmail.com",
        "password": "alkdjnfklasd",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_user2 = requests.post(
        f"{url}auth/register/v2", json=payload_user_2)
    response_user2_data = response_user2.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    payload_removeowner = {
        "token": response_user_data.get('token'),
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": response_user2_data.get('auth_user_id')  # U Id 1
    }

    response_removeowner = requests.post(
        f"{url}channel/removeowner/v1", json=payload_removeowner)
    response_removeowner_data = response_removeowner.json()

    assert response_removeowner_data.get('code') == 400


def test_http_last_owner_in_channel(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_user_2 = {
        "email": "valid2@gmail.com",
        "password": "alkdjnfklasd",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_user2 = requests.post(
        f"{url}auth/register/v2", json=payload_user_2)
    response_user2_data = response_user2.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    payload_user2_joining_channel = {
        "token": response_user2_data.get('token'),
        "channel_id": response_channel_data.get('channel_id')
    }

    requests.post(f"{url}channel/join/v2", json=payload_user2_joining_channel)

    payload_removeowner = {
        "token": response_user_data.get('token'),
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        # U Id 0 BUT they are the only OWNER
        "u_id": response_user_data.get('auth_user_id')
    }

    response_removeowner = requests.post(
        f"{url}channel/removeowner/v1", json=payload_removeowner)
    response_removeowner_data = response_removeowner.json()

    assert response_removeowner_data.get('code') == 400


def test_http_non_owner_trying_to_removeowner(clear_data_http):

    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_user_2 = {
        "email": "valid2@gmail.com",
        "password": "alkdjnfklasd",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_user2 = requests.post(
        f"{url}auth/register/v2", json=payload_user_2)
    response_user2_data = response_user2.json()

    payload_user_3 = {
        "email": "differnt@gmail.com",
        "password": "alkdjnfklasd",
        "name_first": "Pranav",
        "name_last": "Mangla"
    }
    response_user3 = requests.post(
        f"{url}auth/register/v2", json=payload_user_3)
    response_user3_data = response_user3.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    payload_user2_joining_channel = {
        "token": response_user2_data.get('token'),
        "channel_id": response_channel_data.get('channel_id')
    }

    requests.post(f"{url}channel/join/v2", json=payload_user2_joining_channel)

    payload_user3_joining_channel = {
        "token": response_user3_data.get('token'),
        "channel_id": response_channel_data.get('channel_id')
    }

    requests.post(f"{url}channel/join/v2", json=payload_user3_joining_channel)

    payload_addowner_channel = {
        "token": response_user_data.get('token'),  # owner adds u id 2 as owner
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": response_user3_data.get('auth_user_id')  # U Id 2
    }

    requests.post(f"{url}channel/addowner/v1", json=payload_addowner_channel)

    payload_removeowner = {
        # u id 1 NONOWNER trying to remove an owner
        "token": response_user2_data.get('token'),
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": response_user3_data.get('auth_user_id')  # u id 2
    }

    response_removeowner = requests.post(
        f"{url}channel/removeowner/v1", json=payload_removeowner)
    response_removeowner_data = response_removeowner.json()

    assert response_removeowner_data.get('code') == 403


def test_caller_is_not_in_channel(clear_data_http):

    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_user_2 = {
        "email": "valid2@gmail.com",
        "password": "alkdjnfklasd",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_user2 = requests.post(
        f"{url}auth/register/v2", json=payload_user_2)
    response_user2_data = response_user2.json()

    payload_user_3 = {
        "email": "differnt@gmail.com",
        "password": "alkdjnfklasd",
        "name_first": "Pranav",
        "name_last": "Mangla"
    }
    response_user3 = requests.post(
        f"{url}auth/register/v2", json=payload_user_3)
    response_user3_data = response_user3.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    payload_user3_joining_channel = {
        "token": response_user3_data.get('token'),
        "channel_id": response_channel_data.get('channel_id')
    }

    requests.post(f"{url}channel/join/v2", json=payload_user3_joining_channel)

    payload_addowner_channel = {
        "token": response_user_data.get('token'),  # U Id 0
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": response_user3_data.get('auth_user_id')  # U Id 2
    }

    requests.post(f"{url}channel/addowner/v1", json=payload_addowner_channel)

    payload_removeowner = {
        # user isnt EVEN in the channel
        "token": response_user2_data.get('token'),
        "channel_id": response_channel_data.get('channel_id'),
        "u_id": response_user3_data.get('auth_user_id')  # U Id 2
    }

    response_removeowner = requests.post(
        f"{url}channel/removeowner/v1", json=payload_removeowner)
    response_removeowner_data = response_removeowner.json()

    assert response_removeowner_data.get('code') == 403
