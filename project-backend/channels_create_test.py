import pytest

from src.auth import auth_register_v2
from src.error import InputError, AccessError
# from src.channels import channels_create_v1
from src.data_store import data_store
import requests
from src.config import url

# ############ Iteration 1 tests
# # No auth_user_id
# def test_no_auth_user_id(clear_data):
#     auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li").get("auth_user_id")
#     with pytest.raises(AccessError):
#         channels_create_v1(None, "Hello", True)

# # Invalid (negative) auth_user_id
# def test_bad_auth_user_id(clear_data):
#     auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li").get("auth_user_id")
#     with pytest.raises(AccessError):
#         channels_create_v1(-1, "Hello", True)

# # Daniel: If both auth_user_id and is_public is invalid, should throw AccessError
# def test_bad_id_and_bad_is_public(clear_data):
#     auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li").get("auth_user_id")
#     with pytest.raises(AccessError):
#         channels_create_v1(-1, "Hello", "True")

# # Less than 1 character in name
# def test_no_channel_name(clear_data):
#     auth_user_ID = auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li").get("auth_user_id")
#     with pytest.raises(InputError):
#         channels_create_v1(auth_user_ID, None, True)

# # Empty string for name
# def test_channels_create_name_length_1(clear_data):
#     auth_id = auth_register_v2('limelord12490@gmail.com', 'password', 'first', 'last')
#     with pytest.raises(InputError):
#         channels_create_v1(auth_id['auth_user_id'], '', True)

# # More than 20 character in name
# def test_more_than_20_channel_name(clear_data):
#     auth_user_ID = auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li").get("auth_user_id")
#     with pytest.raises(InputError):
#         channels_create_v1(auth_user_ID, "wqwrwerwerqwewewewfewfefwfqwdqwqwd", True)

# # Passes in invalid data type for is_public
# def test_invalid_data_type(clear_data):
#     auth_user_ID = auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li").get("auth_user_id")
#     with pytest.raises(InputError):
#         channels_create_v1(auth_user_ID, "Hello", "True")


# # Testing true for correct channel ID
# def test_true_for_channel_id(clear_data):
#     auth_user_ID = auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li").get("auth_user_id")

#     assert channels_create_v1(auth_user_ID ,"C1", True).get('channel_id') == 0

# # Testing correct ID for multiple channels
# def test_muliple_channels_id(clear_data):
#     auth_user_ID = auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id')
#     auth_user_ID_2 = auth_register_v2("valid2@gmail.com", "aBc2932", "Daniel2", "Li2").get('auth_user_id')

#     assert channels_create_v1(auth_user_ID ,"Hello", True).get('channel_id') == 0
#     assert channels_create_v1(auth_user_ID_2 ,"Hello2", False).get('channel_id') == 1

#####################################################################################################
# Ayush's old tests. Commented out becuase they are not blackbox tests and access the datastore.
# These are still working tests.
# def test_one_channel_datastore(clear_data):
#     auth_user_ID = auth_register_v1("valid@gmail.com", "aBc293", "Daniel", "Li").get("auth_user_id")
#     store = data_store.get()
#     channels_create_v1(auth_user_ID ,"C1", True).get('channel_id')
#     assert(store['channel_id'] == [1])
#     assert(store['channel_id'] == [1])
#     assert(store['channel_is_public'] == [True])
#     assert(store['channel_names'] == ['C1'])

# def test_two_channel_datastore(clear_data):
#     auth_user_ID = auth_register_v1("valid@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id')
#     auth_user_ID_2 = auth_register_v1("valid2@gmail.com", "aBc2932", "Daniel2", "Li2").get('auth_user_id')
#     store = data_store.get()
#     channels_create_v1(auth_user_ID ,"Hello", True)
#     channels_create_v1(auth_user_ID_2 ,"Hello2", False)
#     assert(store['channel_id'] == [1, 2])
#     assert(store['channel_names'] == ['Hello', 'Hello2'])
#     assert(store['channel_is_public'] == [True, False])
#     assert(store['channel_members_id'] == [[1], [2]])

################################
# Below are the HTTP tests

def test_http_single_channel(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()
    
    assert response_channel_data.get('channel_id') == 0


def test_http_channel_name_too_long(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }

    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "thenameofthischannelishopeufllymorethan20characterslong",
        "is_public": True
    }

    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    assert response_channel_data.get('code') == 400


def test_http_channel_name_too_small(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }

    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "",
        "is_public": True
    }

    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    assert response_channel_data.get('code') == 400


def test_http_no_channel_name(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }

    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": None,
        "is_public": True
    }

    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    assert response_channel_data.get('code') == 400


def test_http_invalid_datatype_is_public(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }

    response_user = requests.post(
        f"{url}auth/register/v2", json=payload_register_user)
    response_user_data = response_user.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": 'coolkidsclub',
        "is_public": 'True'
    }

    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    assert response_channel_data.get('code') == 400


def test_http_invalid_token(clear_data_http):
    payload_register_user = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }

    requests.post(f"{url}auth/register/v2", json=payload_register_user)

    payload_create_channel = {
        "token": 'thisisthewrongtoken',
        "name": 'coolkidsclub',
        "is_public": True
    }

    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    assert response_channel_data.get('code') == 403
