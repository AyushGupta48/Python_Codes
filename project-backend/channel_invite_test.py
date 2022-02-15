import pytest

from src.auth import auth_register_v2
from src.error import InputError, AccessError
# from src.channels import channels_create_v1
# from src.channel import channel_invite_v1, channel_invite_v2
import requests
from src.data_store import data_store
from src.config import url

# # Access Error - channel_id is valid and the authorised user is not a member of the channel
# def test_Access_error(clear_data):
#     auth_user_ID = auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id') # gives auth_id 1
#     u_ID2 = auth_register_v2("valid2@gmail.com", "aBc2932", "Daniel2", "Li2").get('auth_user_id') # gives u_id 2
#     auth_user_ID3 = auth_register_v2("valid3@gmail.com", "aBc2933", "Daniel3", "Li3").get('auth_user_id') # gives auth_id 3

#     channels_create_v1(auth_user_ID ,"Hello", True).get('channel_id') # channel Id 1
#     channel_ID2 = channels_create_v1(auth_user_ID3 ,"Hello2", False).get('channel_id') # channel Id 2

#     with pytest.raises(AccessError):
#         channel_invite_v1(auth_user_ID, channel_ID2, u_ID2) # no such thing as channel_id 3

# # Channel_id does not refer to a valid channel
# def test_channel_id_not_exist(clear_data):
#     auth_user_ID = auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id') # gives auth_id 1
#     u_ID = auth_register_v2("valid2@gmail.com", "aBc2932", "Daniel2", "Li2").get('auth_user_id') # gives U_id 2
#     channels_create_v1(auth_user_ID ,"Hello", True).get('channel_id') # gives channel_id as 1

#     with pytest.raises(InputError):
#         channel_invite_v1(auth_user_ID, 3, u_ID) # no such thing as channel_id 3

# # u_ID does not refer to a valid user
# def test_u_id_not_exist(clear_data):
#     auth_user_ID = auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id') # gives auth_id 1
#     auth_register_v2("valid2@gmail.com", "aBc2932", "Daniel2", "Li2").get('auth_user_id') # gives U_id 2
#     channel_ID = channels_create_v1(auth_user_ID ,"Hello", True).get('channel_id') # gives channel_id as 1

#     with pytest.raises(InputError):
#         channel_invite_v1(auth_user_ID, channel_ID, 3) # no such thing as ID 3

# # Admin is already a member of the channel
# def test_admin_already_member(clear_data):
#     auth_user_ID = auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id') # gives auth_id 1
#     auth_register_v2("valid2@gmail.com", "aBc2932", "Daniel2", "Li2").get('auth_user_id') # gives U_id 2
#     channel_ID = channels_create_v1(auth_user_ID ,"Hello", True).get('channel_id') # channel Id 1

#     with pytest.raises(InputError):
#         channel_invite_v1(auth_user_ID, channel_ID, auth_user_ID) # auth id is 1 and so is u id so invite wont work

# # Checking if person already exists in channel
# def test_u_id_already_in_channel(clear_data):
#     auth_user_ID = auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id') # gives auth_id 1
#     u_ID = auth_register_v2("valid2@gmail.com", "aBc2932", "Daniel2", "Li2").get('auth_user_id') # gives U_id 2
#     channel_ID = channels_create_v1(auth_user_ID ,"Hello", True).get('channel_id') # channel Id 1

#     channel_invite_v1(auth_user_ID, channel_ID, u_ID)
#     with pytest.raises(InputError):
#         channel_invite_v1(auth_user_ID, channel_ID, u_ID)

################################
# Below are the HTTP tests

# Invalid token inputted


def test_http_invalid_token(clear_data_http):
    payload_invite_user = {
        "token": 0,
        "channel_id": 0,
        "u_id": 0
    }

    response_invite = requests.post(
        f"{url}channel/invite/v2", json=payload_invite_user)
    response_invite_data = response_invite.json()

    assert response_invite_data.get('code') == 403

# Access Error - channel_id is valid but the authorised user is not a member of the channel

def test_http_channel_id_valid_but_auth_member_is_not_in_channel(clear_data_http):
    # Token 1 - Auth
    payload_register_user_1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user_1 = requests.post(
        f"{url}auth/register/v2", json=payload_register_user_1)
    response_user_data_1 = response_user_1.json()

    #Token 1 creates channel id 0
    payload_create_channel_1 = {
        "token": response_user_data_1.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel_1)

    #Token 2 - Member
    payload_register_user_2 = {
        "email": "valid2@gmail.com",
        "password": "aBc2932",
        "name_first": "Ayush",
        "name_last": "Gupta"
    }
    requests.post(f"{url}auth/register/v2", json=payload_register_user_2)

    #Token 3 - Auth
    payload_register_user_3 = {
        "email": "valid3@gmail.com",
        "password": "aBc2933",
        "name_first": "Pranav",
        "name_last": "Mangla"
    }
    response_user_3 = requests.post(
        f"{url}auth/register/v2", json=payload_register_user_3)
    response_user_data_3 = response_user_3.json()

    #Token 3 creates channel id 1
    payload_create_channel_2 = {
        "token": response_user_data_3.get('token'),
        "name": "coolkidsclub2",
        "is_public": True
    }

    requests.post(f"{url}channels/create/v2", json=payload_create_channel_2)

    payload_invite_user = {
        "token": response_user_data_1.get('token'),
        "channel_id": 1,
        "u_id": 1
    }
    response_invite = requests.post(
        f"{url}channel/invite/v2", json=payload_invite_user)
    response_invite_data = response_invite.json()

    print(response_invite_data)

    assert response_invite_data.get('code') == 403

# u_ID does not refer to a valid user


def test_http_invalid_user_id(clear_data_http):
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
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    payload_invite_user = {
        "token": response_user_data.get('token'),
        "channel_id": 1,
        "u_id": 10
    }
    response_invite = requests.post(
        f"{url}channel/invite/v2", json=payload_invite_user)
    response_invite_data = response_invite.json()

    assert response_invite_data.get('code') == 400

# Channel_id does not refer to a valid channel


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

    payload_create_channel = {
        "token": response_user_data.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    payload_register_user_1 = {
        "email": "ayush@gmail.com",
        "password": "aBc293",
        "name_first": "Ayush",
        "name_last": "Gupta"
    }
    requests.post(f"{url}auth/register/v2", json=payload_register_user_1)

    payload_invite_user = {
        "token": response_user_data.get('token'),
        "channel_id": 10,
        "u_id": 1
    }
    response_invite = requests.post(
        f"{url}channel/invite/v2", json=payload_invite_user)
    response_invite_data = response_invite.json()

    assert response_invite_data.get('code') == 400


# Admin is already a member of the channel
def test_http_admin_is_a_member_already(clear_data_http):
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
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    payload_invite_user = {
        "token": response_user_data.get('token'),
        "channel_id": 0,
        "u_id": response_user_data.get('token')
    }
    response_invite = requests.post(
        f"{url}channel/invite/v2", json=payload_invite_user)
    response_invite_data = response_invite.json()

    assert response_invite_data.get('code') == 400

#Person already exists in channel


def test_http_member_already_in_channel(clear_data_http):
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
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    payload_register_user_2 = {
        "email": "valid2@gmail.com",
        "password": "aBc2932",
        "name_first": "Ayush",
        "name_last": "Gupta"
    }
    requests.post(f"{url}auth/register/v2", json=payload_register_user_2)

    payload_invite_user = {
        "token": response_user_data.get('token'),
        "channel_id": 0,
        "u_id": 1
    }
    requests.post(f"{url}channel/invite/v2", json=payload_invite_user)

    payload_invite_user_again = {
        "token": response_user_data.get('token'),
        "channel_id": 0,
        "u_id": 1
    }
    response_invite_again = requests.post(
        f"{url}channel/invite/v2", json=payload_invite_user_again)
    response_invite_data_again = response_invite_again.json()

    assert response_invite_data_again.get('code') == 400


####################################################################################################################################
#Below are Ayush's good tests. They are commented out becuase they are not black box

# # Adding 1 person into channel
# def test_add_person_into_channel(clear_data):
#     auth_user_ID = auth_register_v1("valid@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id') # gives auth_id 1
#     u_ID = auth_register_v1("valid2@gmail.com", "aBc2932", "Daniel2", "Li2").get('auth_user_id') # gives U_id 2
#     channel_ID = channels_create_v1(auth_user_ID ,"Hello", True).get('channel_id') # channel Id 1

#     store = data_store.get()
#     #user 1 invites user 2
#     channel_invite_v1(auth_user_ID, channel_ID, u_ID)
#     assert(store['channel_members_id'] == [[1, 2]])

# # Adding multiple people to one channel
# def test_add_multiple_people_into_channel(clear_data):
#     auth_user_ID = auth_register_v1("valid@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id') # gives auth_id 1
#     u_ID = auth_register_v1("valid2@gmail.com", "aBc2932", "Daniel2", "Li2").get('auth_user_id') # gives U_id 2
#     u_ID3 = auth_register_v1("valid3@gmail.com", "aBc2933", "Daniel3", "Li3").get('auth_user_id') # gives U_id 3
#     channel_ID = channels_create_v1(auth_user_ID ,"Hello", True).get('channel_id') # channel Id 1

#     store = data_store.get()
#     #user 1 invites user 2 and 3
#     channel_invite_v1(auth_user_ID, channel_ID, u_ID)
#     channel_invite_v1(auth_user_ID, channel_ID, u_ID3)
#     assert(store['channel_members_id'] == [[1, 2, 3]])

# # 2 owners for 2 channel id. Each owner invites 1 person
# def test_multiple_owners(clear_data):
#     auth_user_ID = auth_register_v1("valid@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id') # gives auth_id 1
#     auth_user_ID2 = auth_register_v1("valid2@gmail.com", "aBc2932", "Daniel2", "Li2").get('auth_user_id') # gives auth_id 2
#     u_ID3 = auth_register_v1("valid3@gmail.com", "aBc2933", "Daniel3", "Li3").get('auth_user_id') # gives U_id 3
#     u_ID4 = auth_register_v1("valid4@gmail.com", "aBc2934", "Daniel4", "Li4").get('auth_user_id') # gives U_id 4
#     channel_ID = channels_create_v1(auth_user_ID ,"Hello", True).get('channel_id') # channel Id 1
#     channel_ID2 = channels_create_v1(auth_user_ID2 ,"Hello2", False).get('channel_id') # channel Id 2

#     # auth 1 created channel 1
#     # auth 2 created channel 2
#     # auth 1 invites u_id 3
#     # auth 2 invited u_id 4

#     store = data_store.get()

#     # auth 1 invites user 3
#     channel_invite_v1(auth_user_ID, channel_ID, u_ID3)
#     assert(store['channel_members_id'] == [[1, 3], [2]])

#     # auth 2 invites user 4
#     channel_invite_v1(auth_user_ID2, channel_ID2, u_ID4)
#     assert(store['channel_members_id'] == [[1, 3], [2, 4]])

# # What if auth 2 makes channel 1
# def test_diff_auth_for_diff_channel_id(clear_data):
#     auth_user_ID = auth_register_v1("valid@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id') # gives auth_id 1
#     auth_user_ID2 = auth_register_v1("valid2@gmail.com", "aBc2932", "Daniel2", "Li2").get('auth_user_id') # gives auth_id 2
#     u_ID3 = auth_register_v1("valid3@gmail.com", "aBc2933", "Daniel3", "Li3").get('auth_user_id') # gives U_id 3
#     u_ID4 = auth_register_v1("valid4@gmail.com", "aBc2934", "Daniel4", "Li4").get('auth_user_id') # gives U_id 4
#     channel_ID1 = channels_create_v1(auth_user_ID2 ,"Hello", True).get('channel_id') # channel Id 1
#     channel_ID2 = channels_create_v1(auth_user_ID ,"Hello2", False).get('channel_id') # channel Id 2

#     # auth 1 created channel 2
#     # auth 2 created channel 1
#     # auth 1 invites u_id 3
#     # auth 2 invited u_id 4

#     store = data_store.get()

#     # auth 1 invites user 3
#     channel_invite_v1(auth_user_ID, channel_ID2, u_ID3)
#     assert(store['channel_members_id'] == [[2], [1, 3]])

#     # auth 2 invites user 4
#     channel_invite_v1(auth_user_ID2, channel_ID1, u_ID4)
#     assert(store['channel_members_id'] == [[2, 4], [1, 3]])
