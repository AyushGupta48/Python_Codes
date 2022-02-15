import pytest
import requests
from src.config import url


def test_http_invalid_token(clear_data_http):

    payload_register_user = {  # This person by default has a global permission_id of 1
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
    response_user2 = requests.post(
        f"{url}auth/register/v2", json=payload_user_2)
    response_user2_data = response_user2.json()

    payload_admin_userpermission_change = {
        "token": "invalidtoken",
        "u_id": response_user2_data.get('auth_user_id'),
        "permission_id": 1
    }
    response_userpermission = requests.post(f"{url}admin/userpermission/change/v1",
                                            json=payload_admin_userpermission_change)
    response_userpermission_data = response_userpermission.json()

    assert response_userpermission_data.get('code') == 403


def test_http_non_global_owner(clear_data_http):

    payload_register_user = {  # This person by default has a global permission_id of 1 (Global Owner)
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
    response_user2 = requests.post(
        f"{url}auth/register/v2", json=payload_user_2)
    response_user2_data = response_user2.json()

    payload_user_3 = {
            "email": "valid3@gmail.com",
            "password": "coolpassword",
            "name_first": "Pranav",
            "name_last": "Mangla"
    }
    response_user3 = requests.post(
        f"{url}auth/register/v2", json=payload_user_3)
    response_user3_data = response_user3.json()

    payload_admin_userpermission_change = {
        "token": response_user3_data.get('token'),
        "u_id": response_user2_data.get('auth_user_id'),
        "permission_id": 1
    }
    response_userpermission = requests.post(f"{url}admin/userpermission/change/v1",
                                            json=payload_admin_userpermission_change)
    response_userpermission_data = response_userpermission.json()

    assert response_userpermission_data.get('code') == 403


def test_http_invalid_user_id(clear_data_http):

    payload_register_user = {  # This person by default has a global permission_id of 1
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

    payload_admin_userpermission_change = {
        "token": response_user_data.get('token'),
        "u_id": 12873,  # Invalid user_id
        "permission_id": 1
    }
    response_userpermission = requests.post(f"{url}admin/userpermission/change/v1",
                                            json=payload_admin_userpermission_change)
    response_userpermission_data = response_userpermission.json()

    assert response_userpermission_data.get('code') == 400


def test_http_trying_to_demote_last_global(clear_data_http):

    payload_register_user = {  # This person by default has a global permission_id of 1
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_admin_userpermission_change = {
        "token": response_user_data.get('token'),
        "u_id": response_user_data.get('auth_user_id'),
        # Stream owner attempting to demote himself but he is that last global owner
        "permission_id": 2
    }

    response_userpermission = requests.post(f"{url}admin/userpermission/change/v1",
                                            json=payload_admin_userpermission_change)
    response_userpermission_data = response_userpermission.json()

    assert response_userpermission_data.get('code') == 400


def test_http_invalid_permission_id(clear_data_http):

    payload_register_user = {  # This person by default has a global permission_id of 1
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

    payload_admin_userpermission_change = {
        "token": response_user_data.get('token'),
        "u_id": response_user2_data.get('auth_user_id'),
        "permission_id": 623        # Currently only permission ids 1,2 are defined
    }
    response_userpermission = requests.post(f"{url}admin/userpermission/change/v1",
                                            json=payload_admin_userpermission_change)
    response_userpermission_data = response_userpermission.json()

    assert response_userpermission_data.get('code') == 400


def test_http_valid_permission_changes(clear_data_http):

    payload_register_user = {  # This person by default has a global permission_id of 1
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

    payload_admin_userpermission_change = {
        "token": response_user_data.get('token'),
        "u_id": response_user2_data.get('auth_user_id'),
        "permission_id": 1
    }
    response_userpermission = requests.post(f"{url}admin/userpermission/change/v1",
                                            json=payload_admin_userpermission_change)
    assert response_userpermission.status_code == 200

    payload_second_user_changes_permissions = {
        "token": response_user2_data.get('token'),
        "u_id": response_user_data.get('auth_user_id'),
        "permission_id": 2
    }

    response_second_change = requests.post(f"{url}admin/userpermission/change/v1",
                                           json=payload_second_user_changes_permissions)

    assert response_second_change.status_code == 200
