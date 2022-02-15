import pytest

import requests
from src.config import url


def test_http_invalid_token(clear_data_http):
    list_payload = {
        "token": 0
    }
    response_list = requests.get(
        f"{url}dm/list/v1", params=list_payload).json()

    assert response_list.get('code') == 403


def test_http_no_dms_created(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload1).json()

    list_payload = {
        "token": response_register.get('token')
    }
    response_list = requests.get(
        f"{url}dm/list/v1", params=list_payload).json()

    assert response_list.get('dms') == []


def test_http_not_part_of_dms(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload1).json()

    payload2 = {
        "email": "valid@2gmail.com",
        "password": "aBc293",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    requests.post(f"{url}auth/register/v2", json=payload2).json()

    payload_create = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create).json()

    payload3 = {
        "email": "valid3@gmail.com",
        "password": "aBc293",
        "name_first": "Pranav",
        "name_last": "Mangla"
    }
    response_register3 = requests.post(
        f"{url}auth/register/v2", json=payload3).json()

    list_payload = {
        "token": response_register3.get('token')
    }
    response_list = requests.get(
        f"{url}dm/list/v1", params=list_payload).json()

    assert response_list.get('dms') == []


def test_http_dm_list_success(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload1).json()

    payload2 = {
        "email": "valid@2gmail.com",
        "password": "aBc293",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    requests.post(f"{url}auth/register/v2", json=payload2).json()

    payload_create = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create).json()

    list_payload = {
        "token": response_register.get('token')
    }
    response_list = requests.get(
        f"{url}dm/list/v1", params=list_payload).json()

    assert response_list.get('dms') == [
                             {'dm_id': 0, 'name': "danielli, vikramsundar"}]


def test_http_multiple_dm_list_success(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload1).json()

    payload2 = {
        "email": "valid@2gmail.com",
        "password": "aBc293",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    requests.post(f"{url}auth/register/v2", json=payload2).json()

    payload_create = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create).json()

    payload3 = {
        "email": "valid3@gmail.com",
        "password": "aBc293",
        "name_first": "Pranav",
        "name_last": "Mangla"
    }
    response_register3 = requests.post(
        f"{url}auth/register/v2", json=payload3).json()

    payload_create2 = {
        "token": response_register3.get('token'),
        "u_ids": [0]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create2)

    payload_create3 = {
        "token": response_register3.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create3)

    list_payload = {
        "token": response_register3.get("token")
    }
    response_list = requests.get(
        f"{url}dm/list/v1", params=list_payload).json()
        
    assert response_list.get('dms') == [{'dm_id': 1, 'name': "danielli, pranavmangla"}, {
                             'dm_id': 2, 'name': "pranavmangla, vikramsundar"}]
