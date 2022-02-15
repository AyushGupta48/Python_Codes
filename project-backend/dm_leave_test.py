import pytest
import requests
from src.config import url


def test_http_invalid_token(clear_data_http):
    leave_payload = {
        "token": 0,
        "dm_id": 0
    }
    response_leave = requests.post(
        f"{url}dm/leave/v1", json=leave_payload).json()

    assert response_leave.get('code') == 403


def test_http_invalid_dm_id(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload1).json()

    payload2 = {
        "email": "valid2@gmail.com",
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

    leave_payload = {
        "token": response_register.get('token'),
        "dm_id": 10
    }
    response_leave = requests.post(
        f"{url}dm/leave/v1", json=leave_payload).json()

    assert response_leave.get('code') == 400


def test_http_not_a_member(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload1).json()

    payload2 = {
        "email": "valid2@gmail.com",
        "password": "aBc293",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    requests.post(f"{url}auth/register/v2", json=payload2).json()

    payload3 = {
        "email": "valid3@gmail.com",
        "password": "aBc293",
        "name_first": "Dingus",
        "name_last": "Sundar"
    }
    request = requests.post(f"{url}auth/register/v2", json=payload3).json()

    payload_create = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create).json()

    leave_payload = {
        "token": request.get('token'),
        "dm_id": 0
    }
    response_leave = requests.post(
        f"{url}dm/leave/v1", json=leave_payload).json()

    assert response_leave.get('code') == 403


def test_http_successful_leave(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload1).json()

    payload2 = {
        "email": "valid2@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_register2 = requests.post(
        f"{url}auth/register/v2", json=payload2).json()

    payload_create = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(f"{url}dm/create/v1", json=payload_create).json()

    leave_payload = {
        "token": response_register.get("token"),
        "dm_id": 0
    }
    requests.post(f"{url}dm/leave/v1", json=leave_payload).json()

    list_payload = {
        "token": response_register2.get("token"),
        "dm_id": 0
    }
    response_list = requests.get(
        f"{url}dm/details/v1", params=list_payload).json()
        
    assert response_list.get("name") == "danielli, vikramsundar"
    assert response_list.get("members") == [
                             {"u_id": 1, "email": "valid2@gmail.com", "name_first": "Daniel", "name_last": "Li", "handle_str": "danielli"}]
