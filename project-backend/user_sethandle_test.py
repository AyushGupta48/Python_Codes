import pytest

import requests
from src.config import url


def test_http_invalid_token(clear_data_http):
    handle_change_payload = {
        "token": 0,
        "handle_str": "dingus"
    }
    response_user = requests.put(
        f"{url}user/profile/sethandle/v1", json=handle_change_payload).json()

    assert response_user.get('code') == 403

# Handle length < 3


def test_http_handle_short(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    handle_change_payload = {
        "token": response_register.get('token'),
        "handle_str": "d"
    }
    response_user = requests.put(
        f"{url}user/profile/sethandle/v1", json=handle_change_payload).json()

    assert response_user.get('code') == 400

# Handle length > 20


def test_http_handle_long(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    handle_change_payload = {
        "token": response_register.get('token'),
        "handle_str": "euiknmdhgjtlksmertinxdaf"
    }
    response_user = requests.put(
        f"{url}user/profile/sethandle/v1", json=handle_change_payload).json()

    assert response_user.get('code') == 400


def test_http_non_alphanumeric(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    handle_change_payload = {
        "token": response_register.get('token'),
        "handle_str": "dkjsafnasd@kadfalksd!!"
    }
    response_user = requests.put(
        f"{url}user/profile/sethandle/v1", json=handle_change_payload).json()

    assert response_user.get('code') == 400


def test_http_handle_already_used(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    payload_register = {
        "email": "valid2@gmail.com",
        "password": "abcdef",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    handle_change_payload = {
        "token": response_register.get('token'),
        "handle_str": "danielli"
    }
    response_user = requests.put(
        f"{url}user/profile/sethandle/v1", json=handle_change_payload).json()

    assert response_user.get('code') == 400


def test_http_handle_correct(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    handle_change_payload = {
        "token": response_register.get('token'),
        "handle_str": "danielli"
    }
    requests.put(f"{url}user/profile/sethandle/v1",
                 json=handle_change_payload).json()

    user_check = requests.get(
        f"{url}user/profile/v1", params={"token": response_register.get('token'), "u_id": 0}).json()
    assert user_check == {"user": {"u_id": 0, "email": "valid@gmail.com",
                          "name_first": "Vikram", "name_last": "Sundar", "handle_str": "danielli"}}


def test_http_non_alpha_handle(clear_data_http):
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()

    handle_change_payload = {
        "token": response_register.get('token'),
        "handle_str": "d@n1e!!i"
    }
    response = requests.put(
        f"{url}user/profile/sethandle/v1", json=handle_change_payload).json()

    assert response.get('code') == 400


# def test_http_handle_in_dm(clear_data_http):
#     payload_register = {
#         "email": "valid@gmail.com",
#         "password": "abcdef",
#         "name_first": "Vikram",
#         "name_last": "Sundar"
#     }
#     response_register = requests.post(
#         f"{url}auth/register/v2", json=payload_register).json()
#
#     payload_register2 = {
#         "email": "valid2@gmail.com",
#         "password": "abcdef",
#         "name_first": "Daniel",
#         "name_last": "Li"
#     }
#     requests.post(f"{url}auth/register/v2", json=payload_register2).json()
#
#     dm_create_payload = {
#         "token": response_register.get('token'),
#         "u_ids": [1]
#     }
#     requests.post(f"{url}dm/create/v1", json=dm_create_payload).json()
#
#     handle_change_payload = {
#         "token": response_register.get('token'),
#         "handle_str": "dingus"
#     }
#     requests.put(f"{url}user/profile/sethandle/v1", json=handle_change_payload)
#
#     list_payload = {
#         "token": response_register.get('token'),
#         "dm_id": 0
#     }
#     response_list = requests.get(
#         f"{url}dm/details/v1", params=list_payload).json()
#     assert response_list.get("name") == "danielli, dingus"
#     assert response_list.get("members") == [{"u_id": 0, "email": "valid@gmail.com", "name_first": "Vikram",
#                                              "name_last": "Sundar", "handle_str": "dingus"}, {"u_id": 1, "email": "valid2@gmail.com", "name_first": "Daniel",
#                                                                                               "name_last": "Li", "handle_str": "danielli"}]


# def test_handle_not_in_dm(clear_data_http):
#     payload_register = {
#         "email": "valid@gmail.com",
#         "password": "abcdef",
#         "name_first": "Vikram",
#         "name_last": "Sundar"
#     }
#     response_register = requests.post(
#         f"{url}auth/register/v2", json=payload_register).json()
#
#     payload_register2 = {
#         "email": "valid2@gmail.com",
#         "password": "abcdef",
#         "name_first": "Daniel",
#         "name_last": "Li"
#     }
#     requests.post(f"{url}auth/register/v2", json=payload_register2).json()
#
#     payload_register3 = {
#         "email": "valid3@gmail.com",
#         "password": "abcdef",
#         "name_first": "Pranav",
#         "name_last": "Mangla"
#     }
#     response_register3 = requests.post(
#         f"{url}auth/register/v2", json=payload_register3).json()
#
#     dm_create_payload = {
#         "token": response_register.get('token'),
#         "u_ids": [1]
#     }
#     requests.post(f"{url}dm/create/v1", json=dm_create_payload).json()
#
#     dm_create_payload2 = {
#         "token": response_register3.get('token'),
#         "u_ids": [1]
#     }
#     requests.post(f"{url}dm/create/v1", json=dm_create_payload2).json()
#
#     handle_change_payload = {
#         "token": response_register3.get('token'),
#         "handle_str": "abe"
#     }
#     requests.put(f"{url}user/profile/sethandle/v1", json=handle_change_payload)
#
#     list_payload = {
#         "token": response_register.get('token'),
#         "dm_id": 0
#     }
#     response_list = requests.get(
#         f"{url}dm/details/v1", params=list_payload).json()
#     assert response_list.get("name") == "danielli, vikramsundar"
#     assert response_list.get("members") == [{"u_id": 0, "email": "valid@gmail.com", "name_first": "Vikram",
#                                              "name_last": "Sundar", "handle_str": "vikramsundar"}, {"u_id": 1, "email": "valid2@gmail.com", "name_first": "Daniel",
#                                                                                                     "name_last": "Li", "handle_str": "danielli"}]
#
#     list_payload2 = {
#         "token": response_register3.get('token'),
#         "dm_id": 1
#     }
#     response_list2 = requests.get(
#         f"{url}dm/details/v1", params=list_payload2).json()
#     assert response_list2.get("name") == "abe, danielli"
#     assert response_list2.get("members") == [{"u_id": 2, "email": "valid3@gmail.com", "name_first": "Pranav",
#                                               "name_last": "Mangla", "handle_str": "abe"}, {"u_id": 1, "email": "valid2@gmail.com", "name_first": "Daniel",
#                                                                                             "name_last": "Li", "handle_str": "danielli"}]
