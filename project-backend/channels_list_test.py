import pytest

from src.auth import auth_register_v2
from src.error import InputError, AccessError
# from src.channels import channels_create_v1, channels_list_v1
# from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1
import requests
from src.config import url

# # Access error raised when invalid auth_user_id is passed in
# def test_invalid_user_id(clear_data):
#     auth_register_v2("valid@gmail.com", "abcdef", "Chris", "Smith")
#     with pytest.raises(AccessError):
#         channels_list_v1(3)

# # Access error raised when no auth_user_id is passed in
# def test_no_user_id(clear_data):
#     auth_register_v2("valid@gmail.com", "abcdef", "Chris", "Smith")
#     with pytest.raises(AccessError):
#         channels_list_v1(None)

# # Empty list returned when there are no appropriate channels
# def test_no_channels(clear_data):
#     valid_user_id1 = auth_register_v2("valid@gmail.com", "abcdef", "Chris", "Smith").get('auth_user_id')
#     returned_values = channels_list_v1(valid_user_id1)

#     assert(returned_values == {'channels': []})

# # Test when there is one channel in datastore and one channel that is appropriate to be returned
# def test_single_channel(clear_data):
#     valid_user_id = auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla").get('auth_user_id')
#     channels_create_v1(valid_user_id, "channel name", True)
#     returned_value = channels_list_v1(valid_user_id)
#     assert returned_value == {'channels': [{'channel_id': 0, 'name': 'channel name'}]}

# # Test when there are multiple channels in datastore but only one appropriate channel to be returned
# def test_single_channels(clear_data):
#     valid_user_id1 = auth_register_v2("valid@gmail.com", "abcdef", "Chris", "Smith").get('auth_user_id')
#     valid_user_id2 = auth_register_v2("different@gmail.com", "abcdef", "Daniel", "Li").get('auth_user_id')
#     valid_user_id3 = auth_register_v2("same@gmail.com", "abcdef", "Ayush", "Gupta").get('auth_user_id')

#     channels_create_v1(valid_user_id1, "coolchannelName", True)
#     channels_create_v1(valid_user_id2, "Vikram's Paradise", True)
#     channels_create_v1(valid_user_id1, "Chris's Channel", False)
#     channels_create_v1(valid_user_id3, "Basketball Bros", True)

#     returned_values = channels_list_v1(valid_user_id2)

#     assert returned_values == {'channels': [{'channel_id': 1, 'name': "Vikram's Paradise"}]}

# # Test when there are multiple channels in datastore and multiple appropriate channels to be returned
# def test_multiple_channels(clear_data):
#     valid_user_id1 = auth_register_v2("valid@gmail.com", "abcdef", "Chris", "Smith").get('auth_user_id')
#     valid_user_id2 = auth_register_v2("different@gmail.com", "abcdef", "Daniel", "Li").get('auth_user_id')
#     valid_user_id3 = auth_register_v2("same@gmail.com", "abcdef", "Ayush", "Gupta").get('auth_user_id')

#     channels_create_v1(valid_user_id1, "coolchannelName", True)
#     channels_create_v1(valid_user_id2, "Vikram's Paradise", True)
#     channels_create_v1(valid_user_id1, "Chris's Channel", False)
#     channels_create_v1(valid_user_id3, "Basketball Bros", True)

#     returned_values = channels_list_v1(valid_user_id1)

#     assert returned_values == {'channels': [{'channel_id': 0, 'name': 'coolchannelName'}, {'channel_id': 2, 'name': "Chris's Channel"}]}

# def test_multiple_channels_invites_and_join(clear_data):
#     id_daniel = auth_register_v2("daniel@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id')
#     id_pranav = auth_register_v2("pranav@gmail.com", "aBc2932", "Pranav", "Mangla").get('auth_user_id')
#     id_vikram = auth_register_v2("vikram@gmail.com", "aBc2933", "Vikram", "Sundar").get('auth_user_id')
#     id_ayush = auth_register_v2("guptaishot@gmail.com", "aBc2933", "Ayush", "Gupta").get('auth_user_id')
#     id_mike = auth_register_v2("mike123@gmail.com", "aBc2933", "Mike", "Oxlong").get('auth_user_id')
#     id_connie = auth_register_v2("lconnie@gmail.com", "aBc2933", "Connie", "Lingus").get('auth_user_id')
#     id_jenny = auth_register_v2("tallsjenny@gmail.com", "aBc2933", "Jenny", "Talls").get('auth_user_id')

#     channel_id_fans = channels_create_v1(id_jenny ,"comp1531_fans", False).get('channel_id') # channel Id 1
#     channel_id_lads = channels_create_v1(id_mike ,"lads in the hood", True).get('channel_id') # channel Id 2

#     channel_invite_v1(id_jenny, channel_id_fans, id_connie)
#     channel_invite_v1(id_connie, channel_id_fans, id_vikram)
#     channel_invite_v1(id_vikram, channel_id_fans, id_pranav)

#     channel_invite_v1(id_mike, channel_id_lads, id_daniel)
#     channel_invite_v1(id_mike, channel_id_lads, id_pranav)
#     channel_invite_v1(id_daniel, channel_id_lads, id_vikram)
#     channel_invite_v1(id_pranav, channel_id_lads, id_ayush)
#     channel_join_v1(id_connie, channel_id_lads)

#     assert channels_list_v1(id_jenny) == {'channels': [{'channel_id': 0, 'name': 'comp1531_fans'}]}

#     assert channels_list_v1(id_daniel) == \
#     channels_list_v1(id_ayush) == \
#     channels_list_v1(id_mike) == \
#     {'channels': [{'channel_id': 1, 'name': 'lads in the hood'}]}

#     assert channels_list_v1(id_pranav) == \
#     channels_list_v1(id_connie) == \
#     channels_list_v1(id_vikram) == \
#     {'channels': [{'channel_id': 0, 'name': 'comp1531_fans'}, {'channel_id': 1, 'name': 'lads in the hood'}]}

#################
# Below are the HTTP tests


def test_http_single_channel(clear_data_http):
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

    response_list = requests.get(
        f"{url}channels/list/v2?token={response_data1.get('token')}").json()

    assert response_list == {'channels': [
        {'channel_id': 0, 'name': 'channel_name'}]}


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

    response_list = requests.get(f"{url}channels/list/v2?token=0").json()

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

    response_list = requests.get(f"{url}channels/list/v2?token=").json()
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
        f"{url}channels/list/v2?token={response_data1.get('token')}").json()
        
    assert response_list == {'channels': []}


def test_http_single_channels(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Chris",
        "name_last": "Smith"
    }
    response1 = requests.post(f"{url}auth/register/v2", json=payload1)
    response_data1 = response1.json()

    payload2 = {
        "email": "different@gmail.com",
        "password": "abcdef",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response2 = requests.post(f"{url}auth/register/v2", json=payload2)
    response_data2 = response2.json()

    payload3 = {
        "email": "same@gmail.com",
        "password": "abcdef",
        "name_first": "Ayush",
        "name_last": "Gupta"
    }
    response3 = requests.post(f"{url}auth/register/v2", json=payload3)
    response_data3 = response3.json()

    payload4 = {
        "token": response_data1.get('token'),
        "name": "coolchannelName",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload4)

    payload5 = {
        "token": response_data2.get('token'),
        "name": "Vikram's Paradise",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload5)

    payload6 = {
        "token": response_data1.get('token'),
        "name": "Chris's Channel",
        "is_public": False
    }
    requests.post(f"{url}channels/create/v2", json=payload6)

    payload7 = {
        "token": response_data3.get('token'),
        "name": "Basketball Bros",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload7)

    response_list = requests.get(
        f"{url}channels/list/v2?token={response_data2.get('token')}").json()

    assert response_list == {'channels': [
        {'channel_id': 1, 'name': "Vikram's Paradise"}]}
