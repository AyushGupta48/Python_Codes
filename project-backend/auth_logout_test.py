import pytest
import requests
from src.config import url

# Logging one user out, they then should not be able to call any function without logging back in


def test_successful_logout(clear_data_http):
    # First registering two users
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
    requests.post(f"{url}auth/register/v2", json=payload_user_2)

    payload_logout_user1 = {
        "token": response_user_data.get('token')
    }
    requests.post(f"{url}auth/logout/v1", json=payload_logout_user1)

    payload_channel_create_invalid = {
        "token": response_user_data.get('token'),
        "name": 'coolkidsclub',
        "is_public": 'True'
    }
    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_channel_create_invalid)
    response_channel_data = response_channel.json()

    assert response_channel_data.get('code') == 403


def test_invalid_token(clear_data_http):
    # First registering two users
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    requests.post(f"{url}auth/register/v2", json=payload_register_user)

    payload_user_2 = {
        "email": "valid2@gmail.com",
        "password": "alkdjnfklasd",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    requests.post(f"{url}auth/register/v2", json=payload_user_2)

    payload_logout_user1 = {
        "token": "thisisthewrongtoken"
    }
    response_logout = requests.post(
        f"{url}auth/logout/v1", json=payload_logout_user1)
    response_logout_data = response_logout.json()
    
    assert response_logout_data.get('code') == 403
