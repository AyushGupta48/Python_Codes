import pytest

from src.auth import auth_register_v2
from src.error import InputError, AccessError
# from src.channels import channels_create_v1, channels_listall_v1
# from src.channel import channel_join_v1, channel_invite_v1, channel_details_v1
import requests
from src.config import url
from src.data_store import data_store


# ### Need to remove all 'import data_store' from test files

# # First person to join UNSW Streams is the global owner, right now in iteration 1
# # user_id 1 is the global owner as they are the first person to join Streams

# # Invalid auth_user_id entered.
# def test_invalid_auth_user_id(clear_data):
#     user1 = auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla").get('auth_user_id')
#     auth_register_v2("new@gmail.com", "abcdef", "Dan", "Li").get('auth_user_id')                    # User2
#     channel1 = channels_create_v1(user1, 'Chocolate Factory', False).get('channel_id')

#     with pytest.raises(AccessError):
#         channel_join_v1(524, channel1)

# # No user id entered.
# def test_no_auth_user_id(clear_data):
#     user1 = auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla").get('auth_user_id')
#     auth_register_v2("new@gmail.com", "abcdef", "Dan", "Li").get('auth_user_id')                   # User2
#     channel1 = channels_create_v1(user1, 'Chocolate Factory', False).get('channel_id')

#     with pytest.raises(AccessError):
#         channel_join_v1(None, channel1)

# # Non global owner trying to join private channels.
# def test_trying_to_join_private(clear_data):
#     user1 = auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla").get('auth_user_id')
#     user2 = auth_register_v2("new@gmail.com", "abcdef", "Dan", "Li").get('auth_user_id')
#     channel1 = channels_create_v1(user1, 'Chocolate Factory', False).get('channel_id')

#     with pytest.raises(AccessError):
#         channel_join_v1(user2, channel1)

# # Invalid channel_id entered
# def test_invalid_channel_id(clear_data):
#     auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla").get('auth_user_id')           # User1
#     user2 = auth_register_v2("new@gmail.com", "abcdef", "Dan", "Li").get('auth_user_id')
#     channels_create_v1(user2, 'Chocolate Factory', False).get('channel_id')
#     with pytest.raises(InputError):
#         channel_join_v1(user2, 4214)

# # No channel_id entered
# def test_no_channel_id(clear_data):
#     auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla").get('auth_user_id')           # User1
#     user2 = auth_register_v2("new@gmail.com", "abcdef", "Dan", "Li").get('auth_user_id')
#     channels_create_v1(user2, 'Chocolate Factory', False).get('channel_id')
#     with pytest.raises(InputError):
#         channel_join_v1(user2, None)

# # User2 is already in (owner level) his channel
# def test_trying_to_join_own_channel(clear_data):
#     auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla").get('auth_user_id')           # User1
#     user2 = auth_register_v2("new@gmail.com", "abcdef", "Dan", "Li").get('auth_user_id')
#     channel1 = channels_create_v1(user2, 'Chocolate Factory', False).get('channel_id')
#     with pytest.raises(InputError):
#         channel_join_v1(user2, channel1)

# # User 3 is trying to join a channel to which he already got invited to.
# def test_already_member_in_channel(clear_data):
#     auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla").get('auth_user_id')           # User1
#     user2 = auth_register_v2("new@gmail.com", "123fa3", "Dan", "Li").get('auth_user_id')
#     user3 = auth_register_v2("super@cool.com", "n123bno34", "Ayush", "Gupta").get('auth_user_id')
#     channel1 = channels_create_v1(user2, 'Chocolate Factory', False).get('channel_id')
#     channel_invite_v1(user2, channel1, user3)
#     with pytest.raises(InputError):
#         channel_join_v1(user3, channel1)

# # Global owner should be able to join private channels.
# def test_successful_join_private(clear_data):
#     user1 = auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla").get('auth_user_id')
#     user2 = auth_register_v2("new@gmail.com", "abcdef", "Dan", "Li").get('auth_user_id')
#     channel1 = channels_create_v1(user2, 'Chocolate Factory', False).get('channel_id')
#     channel_join_v1(user1, channel1)
#     all_member_info = channel_details_v1(user2, channel1).get('all_members')
#     member_ids = []
#     for member in all_member_info:
#         member_ids.append(member.get('u_id'))

#     assert member_ids == [user2, user1]


# # Testing channel_join on multiple channels and members
# def test_successful_join_more_complex(clear_data):
#     user1 = auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla").get('auth_user_id')
#     user2 = auth_register_v2("new@gmail.com", "123fa3", "Dan", "Li").get('auth_user_id')
#     user3 = auth_register_v2("super@cool.com", "n123bno34", "Ayush", "Gupta").get('auth_user_id')
#     user4 = auth_register_v2("sad@happy.com", "n123b2345no34", "Chris", "Smith").get('auth_user_id')
#     user5 = auth_register_v2("key@board.com", "aweofjn123bno34", "Vikram", "Sundar").get('auth_user_id')

#     channel1 = channels_create_v1(user2, 'Chocolate Factory', True).get('channel_id')
#     channel2 = channels_create_v1(user4, 'Running CLub', True).get('channel_id')
#     channel3 = channels_create_v1(user5, 'Only Vikram allowed', False).get('channel_id')
#     channel_join_v1(user5, channel1)
#     channel_join_v1(user1, channel1)
#     channel_join_v1(user1, channel2)
#     channel_join_v1(user3, channel2)

#     all_member_info = channel_details_v1(user2, channel1).get('all_members')
#     member_ids = []
#     for member in all_member_info:
#         member_ids.append(member.get('u_id'))

#     assert member_ids == [user2, user5, user1]

#     all_member_info = channel_details_v1(user3, channel2).get('all_members')
#     member_ids = []
#     for member in all_member_info:
#         member_ids.append(member.get('u_id'))

#     assert member_ids == [user4, user1, user3]

#     all_member_info = channel_details_v1(user5, channel3).get('all_members')
#     member_ids = []
#     for member in all_member_info:
#         member_ids.append(member.get('u_id'))

#     assert member_ids == [user5]

##################################
# Below are the HTTP tests

# def test_http_successful_join(clear_data_http):

#     payload_register_user = {
#         "email": "valid@gmail.com",
#         "password": "aBc293",
#         "name_first": "Daniel",
#         "name_last": "Li"
#     }
#     response_user = requests.post(f"{url}auth/register/v2", json=payload_register_user)
#     response_user_data = response_user.json()

#     payload_user_2 = {
#         "email": "valid2@gmail.com",
#         "password": "alkdjnfklasd",
#         "name_first": "Vikram",
#         "name_last": "Sundar"
#     }
#     response2 = requests.post(f"{url}auth/register/v2", json=payload_user_2)
#     response_data2 = response2.json()

#     payload_create_channel = {
#         "token": response_user_data.get('token'),
#         "name": "coolkidsclub",
#         "is_public": True
#     }
#     response_channel = requests.post(f"{url}channels/create/v2", json=payload_create_channel)
#     response_channel_data = response_channel.json()
#     payload_user2_joining_channel = {
#         "token": response_data2.get('token'),
#         "channel_id": 0 #response_channel_data.get('channel_id')
#     }

#     response_join = requests.post(f"{url}channel/join/v2", json=payload_user2_joining_channel)
#     response_join_data = response_join.json()

#     store = data_store.get()
#     print(store)
#     assert store['channel_members_id'] == [[0,1]]

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
    requests.post(f"{url}auth/register/v2", json=payload_user_2)

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()
    payload_user2_joining_channel = {
        "token": "thisisthewrongtoken",
        "channel_id": response_channel_data.get('channel_id')
    }

    response_join = requests.post(
        f"{url}channel/join/v2", json=payload_user2_joining_channel)
    response_join_data = response_join.json()
    
    assert response_join_data.get('code') == 403


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
    response2 = requests.post(f"{url}auth/register/v2", json=payload_user_2)
    response_data2 = response2.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    payload_user2_joining_channel = {
        "token": response_data2.get('token'),
        "channel_id": 324
    }

    response_join = requests.post(
        f"{url}channel/join/v2", json=payload_user2_joining_channel)
    response_join_data = response_join.json()

    assert response_join_data.get('code') == 400


def test_http_already_member(clear_data_http):
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

    payload_user1_joining_channel_invalid = {
        "token": response_user_data.get('token'),
        "channel_id": response_channel_data.get('channel_id')
    }

    response_join = requests.post(
        f"{url}channel/join/v2", json=payload_user1_joining_channel_invalid)
    response_join_data = response_join.json()

    assert response_join_data.get('code') == 400


def test_invalid_non_global_owner_join_private(clear_data_http):
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
    response2 = requests.post(f"{url}auth/register/v2", json=payload_user_2)
    response_data2 = response2.json()

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": False
    }
    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()
    payload_user2_joining_channel = {
        "token": response_data2.get('token'),
        "channel_id": response_channel_data.get('channel_id')
    }

    response_join = requests.post(
        f"{url}channel/join/v2", json=payload_user2_joining_channel)
    response_join_data = response_join.json()

    assert response_join_data.get('code') == 403

# def test_global_joining_private(clear_data_http):

#     payload_register_user = {
#         "email": "valid@gmail.com",
#         "password": "aBc293",
#         "name_first": "Daniel",
#         "name_last": "Li"
#     }
#     response_user = requests.post(f"{url}auth/register/v2", json=payload_register_user)
#     response_user_data = response_user.json()

#     payload_user_2 = {
#         "email": "valid2@gmail.com",
#         "password": "alkdjnfklasd",
#         "name_first": "Vikram",
#         "name_last": "Sundar"
#     }
#     response2 = requests.post(f"{url}auth/register/v2", json=payload_user_2)
#     response_data2 = response2.json()

#     payload_create_channel = {          # Id 2 creates private channel
#         "token": response_data2.get('token'),
#         "name": "coolkidsclub",
#         "is_public": False
#     }
#     response_channel = requests.post(f"{url}channels/create/v2", json=payload_create_channel)
#     response_channel_data = response_channel.json()
#     payload_user1_joining_channel = {           # Id 0 (global owner) joining private
#         "token": response_user_data.get('token'),
#         "channel_id": response_channel_data.get('channel_id')
#     }

#     response_join = requests.post(f"{url}channel/join/v2", json=payload_user1_joining_channel)
#     response_join_data = response_join.json()

#     store = data_store.get() # Need to remove once other functions are wrapped

#     assert store['channel_members_id'] == [1,0]
