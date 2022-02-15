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
        "token": "ivnalidtoken",
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": response_user2_data.get('auth_user_id')  # U Id 1
    }

    response_addowner = requests.post(
        f"{url}channel/addowner/v1", json=payload_addowner_channel)
    response_addowner_data = response_addowner.json()

    assert response_addowner_data.get('code') == 403


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
        "channel_id": 234123,  # C Id 0
        "u_id": response_user2_data.get('auth_user_id')  # U Id 1
    }

    response_addowner = requests.post(
        f"{url}channel/addowner/v1", json=payload_addowner_channel)
    response_addowner_data = response_addowner.json()

    assert response_addowner_data.get('code') == 400


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
        "u_id": 12373  # U Id 1
    }

    response_addowner = requests.post(
        f"{url}channel/addowner/v1", json=payload_addowner_channel)
    response_addowner_data = response_addowner.json()

    assert response_addowner_data.get('code') == 400


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

    payload_addowner_channel = {
        "token": response_user_data.get('token'),
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": response_user2_data.get('auth_user_id')  # U Id 1
    }

    response_addowner = requests.post(
        f"{url}channel/addowner/v1", json=payload_addowner_channel)
    response_addowner_data = response_addowner.json()

    assert response_addowner_data.get('code') == 400


def test_http_user_already_owner_id(clear_data_http):
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

    response_addowner = requests.post(
        f"{url}channel/addowner/v1", json=payload_addowner_channel)
    response_addowner_data = response_addowner.json()

    assert response_addowner.status_code == 200

    # Trying to add the same person (now an owner) as an owner again
    response_addowner = requests.post(
        f"{url}channel/addowner/v1", json=payload_addowner_channel)
    response_addowner_data = response_addowner.json()

    assert response_addowner_data.get('code') == 400


def test_non_owner_trying_to_addowner(clear_data_http):

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
        "token": response_user2_data.get('token'),  # NON OWNER calls ADDOWNER
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": response_user3_data.get('auth_user_id')  # U Id 1
    }

    response_addowner = requests.post(
        f"{url}channel/addowner/v1", json=payload_addowner_channel)
    response_addowner_data = response_addowner.json()

    assert response_addowner_data.get('code') == 403


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
        # U Id 1 ISNT EVEN IN THE CHANNEL
        "token": response_user2_data.get('token'),
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": response_user3_data.get('auth_user_id')  # U Id 2
    }

    response_addowner = requests.post(
        f"{url}channel/addowner/v1", json=payload_addowner_channel)
    response_addowner_data = response_addowner.json()

    assert response_addowner_data.get('code') == 403
