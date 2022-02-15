import pytest

from src.auth import auth_register_v2
from src.error import InputError, AccessError
# from src.channels import channels_create_v1, channels_listall_v1
import requests
from src.config import url

# # Chris's user_id is 1, this test is passing in 3 as a user_id
# def test_invalid_user_id(clear_data):
#     valid_user_id1 = auth_register_v2("valid@gmail.com", "abcdef", "Chris", "Smith")
#     with pytest.raises(AccessError):
#         channels_listall_v1(valid_user_id1)

# # Chris's user_id is 1, this test is passing in nothing as a user_id
# def test_no_user_id(clear_data):
#     auth_register_v2("valid@gmail.com", "abcdef", "Chris", "Smith")
#     with pytest.raises(AccessError):
#         channels_listall_v1(None)

# # Testing if channels_listall will a singular channel and its details
# def test_correct_single_channel(clear_data):
#     valid_user_id = auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla").get('auth_user_id')
#     channels_create_v1(valid_user_id, "coolchannelName", True)
#     returned_values = channels_listall_v1(valid_user_id)

#     assert(returned_values == {'channels': [{'channel_id': 0, 'name': 'coolchannelName',},],})

# # Testing if channels_listall will return multiple channels and their details
# def test_correct_multiple_channels(clear_data):
#     valid_user_id1 = auth_register_v2("valid@gmail.com", "abcdef", "Chris", "Smith").get('auth_user_id')
#     valid_user_id2 = auth_register_v2("different@gmail.com", "abcdef", "Daniel", "Li").get('auth_user_id')
#     valid_user_id3 = auth_register_v2("same@gmail.com", "abcdef", "Ayush", "Gupta").get('auth_user_id')

#     channels_create_v1(valid_user_id1, "coolchannelName", True)
#     channels_create_v1(valid_user_id2, "Vikram's Paradise", True)
#     channels_create_v1(valid_user_id1, "Chris's Channel", False)
#     channels_create_v1(valid_user_id3, "Basketball Bros", True)

#     returned_values = channels_listall_v1(valid_user_id2)

#     assert(returned_values == {
#     'channels': [
#     {'channel_id': 0, 'name': 'coolchannelName'},
#     {'channel_id': 1, 'name': "Vikram's Paradise"},
#     {'channel_id': 2, 'name': "Chris's Channel"},
#     {'channel_id': 3, 'name': "Basketball Bros"},],})

# # Testing to see if channels_listall will return an empty list
# def test_no_channels(clear_data):
#     valid_user_id1 = auth_register_v2("valid@gmail.com", "abcdef", "Chris", "Smith").get('auth_user_id')
#     returned_values = channels_listall_v1(valid_user_id1)

#     assert(returned_values == {'channels': []})

#################
# Below are the HTTP tests


def test_http_correct_single_channel(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Pranav",
        "name_last": "Mangla"
    }
    response1 = requests.post(f"{url}auth/register/v2", json=payload1)
    response_data1 = response1.json()

    payload2 = {
        "token": response_data1.get('token'),
        "name": "coolchannelName",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload2)

    response_list = requests.get(
        f"{url}channels/listall/v2?token={response_data1.get('token')}").json()

    assert response_list == {'channels': [
        {'channel_id': 0, 'name': 'coolchannelName', }, ], }


def test_http_invalid_token(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response1 = requests.post(f"{url}auth/register/v2", json=payload1)
    response_data1 = response1.json()

    payload2 = {
        "token": response_data1.get('token'),
        "name": "channel_name",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload2)

    response_list = requests.get(f"{url}channels/listall/v2?token=0").json()

    assert response_list.get('code') == 403


def test_http_no_token(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response1 = requests.post(f"{url}auth/register/v2", json=payload1)
    response_data1 = response1.json()

    payload2 = {
        "token": response_data1.get('token'),
        "name": "channel_name",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload2)

    response_list = requests.get(f"{url}channels/listall/v2?token=").json()

    assert response_list.get('code') == 403


def test_http_no_channels(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response1 = requests.post(f"{url}auth/register/v2", json=payload1)
    response_data1 = response1.json()

    response_list = requests.get(
        f"{url}channels/listall/v2?token={response_data1.get('token')}").json()
        
    assert response_list == {'channels': []}
