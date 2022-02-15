import pytest


from src.error import InputError, AccessError
import requests
from src.data_store import data_store
from src.config import url

# Invalid token inputted

def test_http_invalid_token(clear_data_http):
    payload_search_messages = {
        "token": 0,
        "query_str": "Hello"
    }

    response_search = requests.get(
        f"{url}search/v1", params=payload_search_messages)
    response_search_data = response_search.json()

    assert response_search_data.get('code') == 403

# Input Error - Length of query is 0

def test_http_no_query_str(clear_data_http):
    # Register a token
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()
    
    # Token creates a channel
    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    #Token sends a message into the channel
    message_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "message": "Hello!"
    }
    requests.post(
        f"{url}message/send/v1", json=message_payload).json()
    
    # Token sends a query string with no characters - Input Error
    query_payload = {
        "token": response_register.get('token'),
        "query_str": ""
    }
    response_query = requests.get(
        f"{url}search/v1", params=query_payload).json()
    
    assert response_query.get('code') == 400


# Input Error - Length of query is over 1000

def test_http_length_over_1000_query_str(clear_data_http):
    # Register a token
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()
    
    # Token creates a channel
    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    #Token sends a message into the channel
    message_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "message": "Hello!"
    }
    requests.post(
        f"{url}message/send/v1", json=message_payload).json()
    
    # Token sends a query string with more than 1000 characters - Input Error
    query_payload = {
        "token": response_register.get('token'),
        "query_str": "h" * 1001
    }
    response_query = requests.get(
        f"{url}search/v1", params=query_payload).json()
    
    assert response_query.get('code') == 400

# One user in one channel sends message
def test_one_message_in_channel(clear_data_http):
    # Register a token
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()
    
    # Token creates a channel
    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    #Token sends a message into the channel
    message_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "message": "Hello!"
    }
    requests.post(
        f"{url}message/send/v1", json=message_payload).json()
    
    # Token sends a query string of He
    query_payload = {
        "token": response_register.get('token'),
        "query_str": "He"
    }
    response_query = requests.get(
        f"{url}search/v1", params=query_payload).json()
    
    assert response_query.get("messages") == ["Hello!"]

# User sends message to 2 different channels he is part of
def test_message_in_multiple_channels(clear_data_http):
    # Register a token
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()
    
    # Token creates a channel
    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    #Token sends a message into the channel
    message_payload = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "message": "Hello!"
    }
    requests.post(
        f"{url}message/send/v1", json=message_payload).json()
    
    # Now token creates a new channel
    payload_create_channel_2 = {
        "token": response_register.get('token'),
        "name": "MySecondChannel",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel_2)

    #Token sends a message into the new channel
    message_payload_2 = {
        "token": response_register.get('token'),
        "channel_id": 1,
        "message": "Hello this is my second channel!"
    }
    requests.post(
        f"{url}message/send/v1", json=message_payload_2).json()

    # Token sends a query string with He
    query_payload = {
        "token": response_register.get('token'),
        "query_str": "He"
    }
    response_query = requests.get(
        f"{url}search/v1", params=query_payload).json()
    
    assert response_query.get("messages") == ["Hello!", "Hello this is my second channel!"]
    
# Someone else in the channel sends a message and the given token can still retrieve this message
# since he is also part of the same channel
def test_someone_else_sends_message_in_channel_with_given_token(clear_data_http):
    
    # Token 0
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()
    
    
    # Token 0 creates a channel 0
    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    # Token 1
    payload_register_2 = {
        "email": "valid2@gmail.com",
        "password": "abcdef",
        "name_first": "Ayush",
        "name_last": "Gupta"
    }
    response_register_2 = requests.post(
        f"{url}auth/register/v2", json=payload_register_2).json()

    #Token 1 joins channel that token 0 made
    payload_join_channel = {
        "token": response_register_2.get('token'),
        "channel_id": 0

    }
    requests.post(
        f"{url}channel/join/v2", json=payload_join_channel).json()

    #Token 1 sends a message into the channel
    message_payload = {
        "token": response_register_2.get('token'),
        "channel_id": 0,
        "message": "Hello!"
    }
    requests.post(
        f"{url}message/send/v1", json=message_payload).json()
    
    
    # Token 0 sends a query string of He
    query_payload = {
        "token": response_register.get('token'),
        "query_str": "He"
    }
    response_query = requests.get(
        f"{url}search/v1", params=query_payload).json()
    
    assert response_query.get("messages") == ["Hello!"]

# Test that it only returns relevant messages
def test_only_return_relevant_message(clear_data_http):
    # Token 0
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()
    
    
    # Token 0 creates a channel 0
    payload_create_channel = {
        "token": response_register.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    # Token 1
    payload_register_2 = {
        "email": "valid2@gmail.com",
        "password": "abcdef",
        "name_first": "Ayush",
        "name_last": "Gupta"
    }
    response_register_2 = requests.post(
        f"{url}auth/register/v2", json=payload_register_2).json()

    #Token 1 joins channel that token 0 made
    payload_join_channel = {
        "token": response_register_2.get('token'),
        "channel_id": 0

    }
    requests.post(
        f"{url}channel/join/v2", json=payload_join_channel).json()

    #Token 1 sends a message into the channel
    message_payload = {
        "token": response_register_2.get('token'),
        "channel_id": 0,
        "message": "Hello!"
    }
    requests.post(
        f"{url}message/send/v1", json=message_payload).json()
    
    message_payload_2 = {
        "token": response_register.get('token'),
        "channel_id": 0,
        "message": "Whats up!"
    }
    requests.post(
        f"{url}message/send/v1", json=message_payload_2).json()
    
    
    # Token 0 sends a query string of He
    query_payload = {
        "token": response_register.get('token'),
        "query_str": "He"
    }
    response_query = requests.get(
        f"{url}search/v1", params=query_payload).json()
    
    assert response_query.get("messages") == ["Hello!"]

# Check if this function also works for dms
def test_for_dms(clear_data_http):
    # Token 0
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()
    
    #token 1
    payload_register_user_2 = {
        "email": "valid2@gmail.com",
        "password": "aBc293",
        "name_first": "Vikram",
        "name_last": "Li"
    }

    requests.post(
        f"{url}auth/register/v2", json=payload_register_user_2).json()

    #Token 0 creates dm with token 1
    payload_create_dm = {
        "token": response_register.get('token'),
        "u_ids": [1]
    }
    requests.post(
        f"{url}dm/create/v1", json=payload_create_dm).json()
    
    send_dm = {
        "token": response_register.get('token'),
        "dm_id": 0,
        "message": "Hello!"
    }
    requests.post(f"{url}message/senddm/v1", json=send_dm)

    # Token 0 sends a query string of He
    query_payload = {
        "token": response_register.get('token'),
        "query_str": "He"
    }
    response_query = requests.get(
        f"{url}search/v1", params=query_payload).json()
    
    assert response_query.get("messages") == ["Hello!"]

# Token 0 is not in channel_id 0, instead he is in channel_id 1
def test_token_in_second_channel(clear_data_http):
    # Token 0
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()
    
    #token 1
    payload_register_user_2 = {
        "email": "valid2@gmail.com",
        "password": "aBc293",
        "name_first": "Vikram",
        "name_last": "Li"
    }

    response_register_2 = requests.post(
        f"{url}auth/register/v2", json=payload_register_user_2).json()

    # token 1 makes channel_id 0
    payload_create_channel = {
        "token": response_register_2.get('token'),
        "name": "coolkidsclub",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel)

    # token 0 makes channel_id 1
    payload_create_channel_2 = {
        "token": response_register.get('token'),
        "name": "second_channel",
        "is_public": True
    }
    requests.post(f"{url}channels/create/v2", json=payload_create_channel_2)

    #Token 0 sends a message into channel_id 1
    message_payload = {
        "token": response_register.get('token'),
        "channel_id": 1,
        "message": "Hello!"
    }
    requests.post(
        f"{url}message/send/v1", json=message_payload).json()

    # Token 0 sends a query string of He
    query_payload = {
        "token": response_register.get('token'),
        "query_str": "He"
    }
    response_query = requests.get(
        f"{url}search/v1", params=query_payload).json()
    
    assert response_query.get("messages") == ["Hello!"]

# Token 0 is not in dm_id 0, instead he is in dm_id 1
def test_token_in_second_dm(clear_data_http):
    # Token 0
    payload_register = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response_register = requests.post(
        f"{url}auth/register/v2", json=payload_register).json()
    
    #token 1
    payload_register_user_2 = {
        "email": "valid2@gmail.com",
        "password": "aBc293",
        "name_first": "Vikram",
        "name_last": "Li"
    }

    response_register_2 = requests.post(
        f"{url}auth/register/v2", json=payload_register_user_2).json()
    
    #token 2
    payload_register_user_3 = {
        "email": "valid3@gmail.com",
        "password": "aBc293",
        "name_first": "Ayush",
        "name_last": "Li"
    }

    requests.post(
        f"{url}auth/register/v2", json=payload_register_user_3).json()

    #Token 1 creates dm_id 0 with token 2
    payload_create_dm = {
        "token": response_register_2.get('token'),
        "u_ids": [2]
    }
    requests.post(
        f"{url}dm/create/v1", json=payload_create_dm).json()

    #Token 0 creates dm_id 1 with token 2
    payload_create_dm_2 = {
        "token": response_register.get('token'),
        "u_ids": [2]
    }
    requests.post(
        f"{url}dm/create/v1", json=payload_create_dm_2).json()
    
    send_dm = {
        "token": response_register.get('token'),
        "dm_id": 1,
        "message": "Hello!"
    }
    requests.post(f"{url}message/senddm/v1", json=send_dm)

    # Token 0 sends a query string of He
    query_payload = {
        "token": response_register.get('token'),
        "query_str": "He"
    }
    response_query = requests.get(
        f"{url}search/v1", params=query_payload).json()
    
    assert response_query.get("messages") == ["Hello!"]
