import pytest

from src.auth import auth_register_v2
from src.error import InputError, AccessError
# from src.channels import channels_create_v1
# from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1, channel_details_v2
import requests
from src.data_store import data_store
from src.config import url

# # Prohibited user tries to call channel_details given.
# def test_channel_id_prohibited(clear_data):
#     auth_user_ID = auth_register_v2("daniel@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id') # gives auth_id 0
#     u_ID = auth_register_v2("pranav@gmail.com", "aBc2932", "Pranav", "Mangla").get('auth_user_id') # gives U_id 1
#     u_ID3 = auth_register_v2("vikram@gmail.com", "aBc2933", "Vikram", "Sundar").get('auth_user_id') # gives U_id 2

#     # Daniel invites Pranav but not Vikram.
#     channel_ID = channels_create_v1(auth_user_ID ,"Bois", True).get('channel_id') # channel Id 0
#     channel_invite_v1(auth_user_ID, channel_ID, u_ID)

#     # Vikram tries to call channel_details for server he is not invited to.
#     with pytest.raises(AccessError):
#         channel_details_v1(u_ID3, channel_ID)

# # Invalid (Non-existent) channel_id given.
# def test_user_id_invalid(clear_data):
#     auth_user_ID = auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id') # gives auth_id 0
#     channels_create_v1(auth_user_ID ,"General", True).get('channel_id') # channel Id 0
#     with pytest.raises(AccessError):
#         channel_details_v1(-1, auth_user_ID)

# # 'None'channel_id given.
# def test_user_id_none(clear_data):
#     auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li") # gives auth_id 0
#     channels_create_v1(0 ,"General", True).get('channel_id') # channel Id 0
#     with pytest.raises(AccessError):
#         channel_details_v1(None, 1)

# # Invalid (Non-existent) channel_id and invalid channel given.
# def test_channel_both_argument_invalid(clear_data):
#     auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li") # gives auth_id 0
#     channels_create_v1(0 ,"General", True).get('channel_id') # channel Id 0
#     with pytest.raises(AccessError):
#         channel_details_v1(1234, 200)

# # Invalid (Negative) channel_id given.
# def test_channel_id_negative(clear_data):
#     auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li") # gives auth_id 0
#     channels_create_v1(0 ,"General", True).get('channel_id') # channel Id 0
#     with pytest.raises(InputError):
#         channel_details_v1(0, -1)

# # Invalid (Non-existent) channel_id given.
# def test_channel_id_invalid(clear_data):
#     auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li") # gives auth_id 0
#     channels_create_v1(0 ,"General", True).get('channel_id') # channel Id 0
#     with pytest.raises(InputError):
#         channel_details_v1(0, 200)

# # 'None' channel_id given.
# def test_channel_id_none(clear_data):
#     auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li") # gives auth_id 0
#     channels_create_v1(0 ,"General", True).get('channel_id') # channel Id 0
#     with pytest.raises(InputError):
#         channel_details_v1(0, None)

# # test one member (owner)
# def test_one_member_details(clear_data):
#     auth_user_ID = auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id') # gives auth_id 0
#     channel_ID = channels_create_v1(auth_user_ID ,"General", True).get('channel_id') # channel Id 0

#     assert channel_details_v1(auth_user_ID, channel_ID) == \
#     {
#         'name': 'General',
#         'is_public': True,
#         'owner_members': [
#             {
#                 'u_id': 0,
#                 'email': 'valid@gmail.com',
#                 'name_first': 'Daniel',
#                 'name_last': 'Li',
#                 'handle_str': 'danielli',
#             }
#         ],
#         'all_members': [
#             {
#                 'u_id': 0,
#                 'email': 'valid@gmail.com',
#                 'name_first': 'Daniel',
#                 'name_last': 'Li',
#                 'handle_str': 'danielli',
#             }
#         ],
#     }

# def test_multiple_member_details(clear_data):
#     auth_user_ID = auth_register_v2("daniel@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id') # gives auth_id 0
#     u_ID2 = auth_register_v2("pranav@gmail.com", "aBc2932", "Pranav", "Mangla").get('auth_user_id') # gives U_id 1
#     u_ID3 = auth_register_v2("vikram@gmail.com", "aBc2933", "Vikram", "Sundar").get('auth_user_id') # gives U_id 2
#     channel_ID = channels_create_v1(auth_user_ID ,"Bois", True).get('channel_id') # channel Id 0

#     #user 1 invites user 2 and 3
#     channel_invite_v1(auth_user_ID, channel_ID, u_ID2)
#     channel_invite_v1(auth_user_ID, channel_ID, u_ID3)

#     assert channel_details_v1(auth_user_ID, channel_ID) == \
#     {
#         'name': 'Bois',
#         'is_public': True,
#         'owner_members': [
#             {
#                 'u_id': 0,
#                 'email': 'daniel@gmail.com',
#                 'name_first': 'Daniel',
#                 'name_last': 'Li',
#                 'handle_str': 'danielli',
#             }
#         ],
#         'all_members': [
#             {
#                 'u_id': 0,
#                 'email': 'daniel@gmail.com',
#                 'name_first': 'Daniel',
#                 'name_last': 'Li',
#                 'handle_str': 'danielli',
#             } ,
#             {
#                 'u_id': 1,
#                 'email': 'pranav@gmail.com',
#                 'name_first': 'Pranav',
#                 'name_last': 'Mangla',
#                 'handle_str': 'pranavmangla',
#             },
#             {
#                 'u_id': 2,
#                 'email': 'vikram@gmail.com',
#                 'name_first': 'Vikram',
#                 'name_last': 'Sundar',
#                 'handle_str': 'vikramsundar',
#             }
#         ],
#     }

# def test_multiple_member_details_private_channel(clear_data):
#     id_daniel = auth_register_v2("daniel@gmail.com", "aBc293", "Daniel", "Li").get('auth_user_id')
#     id_pranav = auth_register_v2("pranav@gmail.com", "aBc2932", "Pranav", "Mangla").get('auth_user_id')
#     id_vikram = auth_register_v2("vikram@gmail.com", "aBc2933", "Vikram", "Sundar").get('auth_user_id')
#     id_ayush = auth_register_v2("guptaishot@gmail.com", "aBc2933", "Ayush", "Gupta").get('auth_user_id')
#     id_mike = auth_register_v2("mike123@gmail.com", "aBc2933", "Mike", "Oxlong").get('auth_user_id')
#     id_connie = auth_register_v2("lconnie@gmail.com", "aBc2933", "Connie", "Lingus").get('auth_user_id')
#     id_jenny = auth_register_v2("tallsjenny@gmail.com", "aBc2933", "Jenny", "Talls").get('auth_user_id')

#     channel_id_fans = channels_create_v1(id_jenny ,"comp1531_fans", False).get('channel_id') # channel Id 0
#     channel_id_lads = channels_create_v1(id_mike ,"lads in the hood", True).get('channel_id') # channel Id 1

#     channel_invite_v1(id_jenny, channel_id_fans, id_connie)
#     channel_invite_v1(id_connie, channel_id_fans, id_vikram)
#     channel_invite_v1(id_vikram, channel_id_fans, id_pranav)

#     channel_invite_v1(id_mike, channel_id_lads, id_daniel)
#     channel_invite_v1(id_mike, channel_id_lads, id_pranav)
#     channel_invite_v1(id_daniel, channel_id_lads, id_vikram)
#     channel_invite_v1(id_pranav, channel_id_lads, id_ayush)
#     channel_join_v1(id_connie, channel_id_lads)

#     assert channel_details_v1(id_vikram, channel_id_lads) == \
#     {
#         'name': 'lads in the hood',
#         'is_public': True,
#         'owner_members': [
#             {
#                 'u_id': 4,
#                 'email': 'mike123@gmail.com',
#                 'name_first': 'Mike',
#                 'name_last': 'Oxlong',
#                 'handle_str': 'mikeoxlong',
#             }
#         ],
#         'all_members': [
#             {
#                 'u_id': 4,
#                 'email': 'mike123@gmail.com',
#                 'name_first': 'Mike',
#                 'name_last': 'Oxlong',
#                 'handle_str': 'mikeoxlong',
#             } ,
#             {
#                 'u_id': 0,
#                 'email': 'daniel@gmail.com',
#                 'name_first': 'Daniel',
#                 'name_last': 'Li',
#                 'handle_str': 'danielli',
#             } ,
#             {
#                 'u_id': 1,
#                 'email': 'pranav@gmail.com',
#                 'name_first': 'Pranav',
#                 'name_last': 'Mangla',
#                 'handle_str': 'pranavmangla',
#             } ,
#             {
#                 'u_id': 2,
#                 'email': 'vikram@gmail.com',
#                 'name_first': 'Vikram',
#                 'name_last': 'Sundar',
#                 'handle_str': 'vikramsundar',
#             } ,
#             {
#                 'u_id': 3,
#                 'email': 'guptaishot@gmail.com',
#                 'name_first': 'Ayush',
#                 'name_last': 'Gupta',
#                 'handle_str': 'ayushgupta',
#             } ,
#             {
#                 'u_id': 5,
#                 'email': 'lconnie@gmail.com',
#                 'name_first': 'Connie',
#                 'name_last': 'Lingus',
#                 'handle_str': 'connielingus',
#             }
#         ]
#     }

#     assert channel_details_v1(id_jenny, channel_id_fans) == \
#     {
#         'name': 'comp1531_fans',
#         'is_public': False,
#         'owner_members': [
#             {
#                 'u_id': 6,
#                 'email': 'tallsjenny@gmail.com',
#                 'name_first': 'Jenny',
#                 'name_last': 'Talls',
#                 'handle_str': 'jennytalls',
#             }
#         ],
#         'all_members': [
#             {
#                 'u_id': 6,
#                 'email': 'tallsjenny@gmail.com',
#                 'name_first': 'Jenny',
#                 'name_last': 'Talls',
#                 'handle_str': 'jennytalls',
#             } ,
#             {
#                 'u_id': 5,
#                 'email': 'lconnie@gmail.com',
#                 'name_first': 'Connie',
#                 'name_last': 'Lingus',
#                 'handle_str': 'connielingus',
#             } ,
#             {
#                 'u_id': 2,
#                 'email': 'vikram@gmail.com',
#                 'name_first': 'Vikram',
#                 'name_last': 'Sundar',
#                 'handle_str': 'vikramsundar',
#             } ,
#             {
#                 'u_id': 1,
#                 'email': 'pranav@gmail.com',
#                 'name_first': 'Pranav',
#                 'name_last': 'Mangla',
#                 'handle_str': 'pranavmangla',
#             }
#         ]
#     }

################################
# Below are the HTTP tests

# Invalid Token


def test_http_invalid_token(clear_data_http):
    payload_channel_details = {
        "token": 0,
        "channel_id": 0
    }

    response_details = requests.get(
        f"{url}channel/details/v2", params=payload_channel_details)
    response_details_data = response_details.json()

    assert response_details_data.get('code') == 403

# Invalid channel_id


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

    payload_channel_details = {
        "token": response_user_data.get('token'),
        "channel_id": 1
    }

    response_details = requests.get(
        f"{url}channel/details/v2", params=payload_channel_details)
    response_details_data = response_details.json()

    assert response_details_data.get('code') == 400


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

    #Token 1 creates channel id 1
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

    #Token 3 creates channel id 2
    payload_create_channel_2 = {
        "token": response_user_data_3.get('token'),
        "name": "coolkidsclub2",
        "is_public": False
    }

    requests.post(f"{url}channels/create/v2", json=payload_create_channel_2)

    payload_channel_details = {
        "token": response_user_data_1.get('token'),
        "channel_id": 1
    }

    response_details = requests.get(
        f"{url}channel/details/v2", params=payload_channel_details)
    response_details_data = response_details.json()

    assert response_details_data.get('code') == 403


def test_http_one_member_details(clear_data_http):
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

    payload_channel_details = {
        "token": response_user_data.get('token'),
        "channel_id": 0
    }

    response_details = requests.get(
        f"{url}channel/details/v2", params=payload_channel_details)
    response_details_data = response_details.json()

    assert response_details_data['name'] == "coolkidsclub"
    assert response_details_data['is_public'] is True
    assert response_details_data['owner_members'] == \
        [{
            'u_id': 0,
            'email': "valid@gmail.com",
            'name_first': "Daniel",
            'name_last': "Li",
            'handle_str': 'danielli'
            }]
    assert response_details_data['all_members'] == \
        [{
            'u_id': 0,
            'email': "valid@gmail.com",
            'name_first': "Daniel",
            'name_last': "Li",
            'handle_str': 'danielli'
            }]

# Test multiple members


def test_http_multiple_member_details(clear_data_http):
    payload_register_user_1 = {
        "email": "daniel@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user_1 = requests.post(
        f"{url}auth/register/v2", json=payload_register_user_1)
    response_user_data_1 = response_user_1.json()

    payload_register_user_2 = {
        "email": "pranav@gmail.com",
        "password": "aBc2932",
        "name_first": "Pranav",
        "name_last": "Mangla"
    }
    requests.post(f"{url}auth/register/v2", json=payload_register_user_2)

    payload_register_user_3 = {
        "email": "vikram@gmail.com",
        "password": "aBc2933",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    requests.post(f"{url}auth/register/v2", json=payload_register_user_3)

    payload_create_channel = {
        "token": response_user_data_1.get('token'),
        "name": "Bois",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    payload_invite_user_1 = {
        "token": response_user_data_1.get('token'),
        "channel_id": 0,
        "u_id": 1
    }
    requests.post(f"{url}channel/invite/v2", json=payload_invite_user_1)

    payload_invite_user_2 = {
        "token": response_user_data_1.get('token'),
        "channel_id": 0,
        "u_id": 2
    }
    requests.post(f"{url}channel/invite/v2", json=payload_invite_user_2)

    payload_channel_details = {
        "token": response_user_data_1.get('token'),
        "channel_id": 0
    }

    response_details = requests.get(
        f"{url}channel/details/v2", params=payload_channel_details)
    response_details_data = response_details.json()

    assert response_details_data['name'] == 'Bois'
    assert response_details_data['is_public'] == True
    assert response_details_data['owner_members'] == \
        [{
            'u_id': 0,
            'email': "daniel@gmail.com",
            'name_first': "Daniel",
            'name_last': "Li",
            'handle_str': 'danielli'
            }]
    assert response_details_data['all_members'] == \
        [{
            'u_id': 0,
            'email': "daniel@gmail.com",
            'name_first': "Daniel",
            'name_last': "Li",
            'handle_str': 'danielli'
            },
         {
            'u_id': 1,
            'email': 'pranav@gmail.com',
            'name_first': 'Pranav',
            'name_last': 'Mangla',
            'handle_str': 'pranavmangla'
            },
         {
            'u_id': 2,
            'email': 'vikram@gmail.com',
            'name_first': 'Vikram',
            'name_last': 'Sundar',
            'handle_str': 'vikramsundar'
            }]

#Multiple owners


def test_http_multiple_owners(clear_data_http):
    payload_register_user_1 = {
        "email": "daniel@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response_user_1 = requests.post(
        f"{url}auth/register/v2", json=payload_register_user_1)
    response_user_data_1 = response_user_1.json()

    payload_register_user_2 = {
        "email": "pranav@gmail.com",
        "password": "aBc2932",
        "name_first": "Pranav",
        "name_last": "Mangla"
    }
    response_user_2 = requests.post(
        f"{url}auth/register/v2", json=payload_register_user_2)
    response_user_data_2 = response_user_2.json()

    payload_register_user_3 = {
        "email": "vikram@gmail.com",
        "password": "aBc2933",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    requests.post(f"{url}auth/register/v2", json=payload_register_user_3)

    payload_register_user_4 = {
        "email": "ayush@gmail.com",
        "password": "aBc2933",
        "name_first": "Ayush",
        "name_last": "Gupta"
    }
    requests.post(f"{url}auth/register/v2", json=payload_register_user_4)

    # U_Id 0 creates channel
    payload_create_channel = {
        "token": response_user_data_1.get('token'),
        "name": "Bois",
        "is_public": True
    }
    response_channel = requests.post(
        f"{url}channels/create/v2", json=payload_create_channel)
    response_channel_data = response_channel.json()

    # U_Id 1 joins channel
    payload_user2_joining_channel = {
        "token": response_user_data_2.get('token'),
        "channel_id": response_channel_data.get('channel_id')
    }
    requests.post(f"{url}channel/join/v2", json=payload_user2_joining_channel)

    #U_id 1 also becomes owner
    payload_addowner_channel = {
        "token": response_user_data_1.get('token'),
        "channel_id": response_channel_data.get('channel_id'),  # C Id 0
        "u_id": 1
    }

    requests.post(f"{url}channel/addowner/v1", json=payload_addowner_channel)

    # U_ID 0 invites u_id 2
    payload_invite_user_3 = {
        "token": response_user_data_1.get('token'),
        "channel_id": 0,
        "u_id": 2
    }
    requests.post(f"{url}channel/invite/v2", json=payload_invite_user_3)

    # U_ID 0 invites u_id 3
    payload_invite_user_4 = {
        "token": response_user_data_1.get('token'),
        "channel_id": 0,
        "u_id": 3
    }
    requests.post(f"{url}channel/invite/v2", json=payload_invite_user_4)

    payload_channel_details = {
        "token": response_user_data_1.get('token'),
        "channel_id": 0
    }

    response_details = requests.get(
        f"{url}channel/details/v2", params=payload_channel_details)
    response_details_data = response_details.json()

    assert response_details_data['name'] == 'Bois'
    assert response_details_data['is_public'] is True
    assert response_details_data['owner_members'] == \
        [{
            'u_id': 0,
            'email': "daniel@gmail.com",
            'name_first': "Daniel",
            'name_last': "Li",
            'handle_str': 'danielli'
            },
         {
            'u_id': 1,
            'email': 'pranav@gmail.com',
            'name_first': 'Pranav',
            'name_last': 'Mangla',
            'handle_str': 'pranavmangla'
            }]
    assert response_details_data['all_members'] == \
        [{
            'u_id': 0,
            'email': "daniel@gmail.com",
            'name_first': "Daniel",
            'name_last': "Li",
            'handle_str': 'danielli'
            },
         {
            'u_id': 1,
            'email': 'pranav@gmail.com',
            'name_first': 'Pranav',
            'name_last': 'Mangla',
            'handle_str': 'pranavmangla'
            },
         {
            'u_id': 2,
            'email': 'vikram@gmail.com',
            'name_first': 'Vikram',
            'name_last': 'Sundar',
            'handle_str': 'vikramsundar'
            },
         {
            'u_id': 3,
            'email': 'ayush@gmail.com',
            'name_first': 'Ayush',
            'name_last': 'Gupta',
            'handle_str': 'ayushgupta'
            }]
