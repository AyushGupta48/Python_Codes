import pytest
import requests
from src.config import url


def test_http_invalid_token(clear_data_http):
    payload_create = {
        "token": 0,
        "u_ids": [1, 2]
    }
    response_create = requests.post(
        f"{url}dm/create/v1", json=payload_create).json()

    assert response_create.get('code') == 403


def test_http_invalid_u_id(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }

    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register_user).json()

    payload_create = {
        "token": response_register.get('token'),
        "u_ids": [1, 2]
    }
    response_create = requests.post(
        f"{url}dm/create/v1", json=payload_create).json()

    assert response_create.get('code') == 400


def test_http_successful_single_dm(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }

    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register_user).json()

    payload_register_user2 = {
        "email": "valid2@gmail.com",
        "password": "aBc293",
        "name_first": "Vikram",
        "name_last": "Li"
    }

    requests.post(f"{url}auth/register/v2", json=payload_register_user2).json()

    payload_create = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    response_create = requests.post(
        f"{url}dm/create/v1", json=payload_create).json()

    assert response_create.get('dm_id') == 0


def test_http_successful_multiple_dm(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }

    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register_user).json()

    payload_register_user2 = {
        "email": "valid2@gmail.com",
        "password": "aBc293",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }

    requests.post(f"{url}auth/register/v2", json=payload_register_user2).json()

    payload_register_user3 = {
        "email": "valid3@gmail.com",
        "password": "aBc293",
        "name_first": "Pranav",
        "name_last": "Mangla"
    }

    requests.post(f"{url}auth/register/v2", json=payload_register_user3).json()

    payload_create = {
        "token": response_register.get('token'),
        "u_ids": [1, 2]
    }
    response_create = requests.post(
        f"{url}dm/create/v1", json=payload_create).json()

    assert response_create.get("dm_id") == 0


def test_http_create_dm_with_creator_id(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }

    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register_user).json()

    payload_create = {
        "token": response_register.get('token'),
        "u_ids": [0]
    }
    response_create = requests.post(
        f"{url}dm/create/v1", json=payload_create).json()

    assert response_create.get('code') == 400


def test_http_create_multiple_dms(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }

    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register_user).json()

    payload_register_user2 = {
        "email": "valid2@gmail.com",
        "password": "aBc293",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }

    requests.post(f"{url}auth/register/v2", json=payload_register_user2).json()

    payload_register_user3 = {
        "email": "valid3@gmail.com",
        "password": "aBc293",
        "name_first": "Pranav",
        "name_last": "Mangla"
    }

    requests.post(f"{url}auth/register/v2", json=payload_register_user3).json()

    payload_create = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    response_create = requests.post(
        f"{url}dm/create/v1", json=payload_create).json()

    assert response_create.get("dm_id") == 0

    payload_create2 = {
        "token": response_register.get('token'),
        "u_ids": [2]
    }
    response_create2 = requests.post(
        f"{url}dm/create/v1", json=payload_create2).json()
        
    assert response_create2.get("dm_id") == 1
