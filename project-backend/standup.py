from _pytest.python_api import raises
from src.error import InputError, AccessError
from src.data_store import data_store
from src.other import decode_jwt
import time

def standup_start(token, channel_id, length):
    store = data_store.get()

    # Valid token check
    if token not in store['user_tokens']:
        raise AccessError(description="Not a valid token")

    # Invalid channel_id check
    if channel_id not in store['channel_id']:
        raise InputError(description="Not a valid channel_id")

    channel_index = store['channel_id'].index(channel_id)
    # Check to see if user is in channel
    if decode_jwt(token).get('username') not in store['channel_members_id'][channel_index]:
        raise AccessError(description=
            "Error: authorised user is not a member of the channel")

    # Check if length of standup is negative or isn't a number
    if not isinstance(length, int) or length < 0:
        raise InputError(description="Invalid length")

    # Check if the channel already has a standup active
    for standup in store['standup_queue']:
        if standup['channel_id'] == channel_id:
            raise InputError(description="Standup already active in channel")

    # Update and generate new standup id
    standup_id = store['standup_tracker'] + 1
    store['standup_tracker'] = standup_id

    time_finish = int(time.time() + length)

    # Finding the position of the user
    u_index = store['user_emails'].index(decode_jwt(token).get('username'))
    u_id = store['user_id'][u_index]

    # Append to the list of standups that are active
    store['standup_queue'].append({'standup_id': standup_id, 'u_id': u_id, 'channel_id': channel_id, 'time_finish': time_finish, 'messages': []})

    data_store.set(store)

    return {'time_finish': time_finish}

def standup_active(token, channel_id):
    store = data_store.get()

    # Valid token check
    if token not in store['user_tokens']:
        raise AccessError(description="Not a valid token")

    # Invalid channel_id check
    if channel_id not in store['channel_id']:
        raise InputError(description="Not a valid channel_id")

    channel_index = store['channel_id'].index(channel_id)
    # Check to see if user is in channel
    if decode_jwt(token).get('username') not in store['channel_members_id'][channel_index]:
        raise AccessError(description=
            "Error: authorised user is not a member of the channel")

    # If we find a standup in the standup queue that actually exists for the channel, we want to return it
    for standup in store['standup_queue']:
        if standup['channel_id'] == channel_id:
            return {'is_active': True, 'time_finish': standup['time_finish']}

    # Otherwise, we default to the following return
    return {
        'is_active': False,
        'time_finish': None
    }

def standup_send(token, channel_id, message):
    store = data_store.get()

    # Valid token check
    if token not in store['user_tokens']:
        raise AccessError(description="Not a valid token")

    # Invalid channel_id check
    if channel_id not in store['channel_id']:
        raise InputError(description="Not a valid channel_id")

    channel_index = store['channel_id'].index(channel_id)
    # Check to see if user is in channel
    if decode_jwt(token).get('username') not in store['channel_members_id'][channel_index]:
        raise AccessError(description=
            "Error: authorised user is not a member of the channel")

    # Check to see if message is too long
    if len(message) > 1000:
        raise InputError(description="Message is too long")

    # Finding the position of the user
    u_index = store['user_emails'].index(decode_jwt(token).get('username'))
    handle = store['user_handles'][u_index]

    active_standup_exists = False
    # If we find a standup in the standup queue that actually exists for the channel, we can add message to it
    for standup in store['standup_queue']:
        if standup['channel_id'] == channel_id:
            message_to_append = handle + ": " + message
            standup['messages'].append(message_to_append)
            active_standup_exists = True
    
    if active_standup_exists is False:
        raise InputError(description="No standup exists in channel")

    data_store.set(store)
    return {}