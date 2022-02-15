from _pytest.python_api import raises
from src.error import InputError, AccessError
from src.data_store import data_store
from src.other import decode_jwt


def admin_userpermission_change_v1(token, u_id, permission_id):
    '''
    admin_userpermission_change_v1 takes in a token, a user's id and a given
    permission_id to change that user to. It can only be successfully called
    by an existing streams owner.

    Arguments:
        token           (string)        -   The token of the authorised user
        u_id            (integer)       -   The id of the user having their permissions updated
        permission_id   (integer)       -   The id of the permission level being granted to the user

    Exceptions:
        InputError      -   Occurs when user_id does not refer to a valid user
                        -   Occurs when permission_id does not refer to a valid permission
                        -   Occurs when attempting to change last global owner to a global member

        AccessError     -   Occurs when an invalid token is entered
                        -   Occurs when the authorised user is not a streams global owner

    Return Value:
        No Return
    '''
    store = data_store.get()

    # Valid token check
    if token not in store['user_tokens']:
        raise AccessError(description='Not a valid token')

    auth_user_index = store['user_emails'].index(
        decode_jwt(token).get('username'))

    # Check if user calling the function is a global owner (has permission id 1)
    if store['user_global_permission_level'][auth_user_index] != 1:
        raise AccessError(description='The authorised user is not a streams global owner')

    # Check if the u_id refers to a valid user
    if u_id not in store['user_id']:
        raise InputError(description='Not a valid user_id')

    if permission_id != 1 and permission_id != 2:
        raise InputError(description='Permission id is invalid')

    u_id_index = store['user_id'].index(u_id)

    # Check if last global owner is trying to demote themselves

    number_of_global_owners = 0
    for user_permission_level in store['user_global_permission_level']:
        if user_permission_level == 1:
            number_of_global_owners += 1

    if number_of_global_owners == 1 and auth_user_index == u_id_index \
            and permission_id == 2:
        raise InputError(description='Cannot change last global owner to a global member')

    # Updating the specified user's global permission level
    store['user_global_permission_level'][u_id_index] = permission_id

    data_store.set(store)

    return {
    }


def admin_userremove_v1(token, u_id):
    '''
    admin_userremove_1 takes in a token, a user's id. It can only be successfully called
    by an existing streams owner.

    Arguments:
        token           (string)        -   The token of the authorised user
        u_id            (integer)       -   The id of the user being removed

    Exceptions:
        InputError      -   Occurs when user_id does not refer to a valid user
                        -   Occurs when attempting to remove last global owner

        AccessError     -   Occurs when an invalid token is entered
                        -   Occurs when the authorised user is not a streams global owner

    Return Value:
        No Return
    '''
    store = data_store.get()

    # Valid token check
    if token not in store['user_tokens']:
        raise AccessError(description='Not a valid token')

    auth_user_index = store['user_emails'].index(
        decode_jwt(token).get('username'))

    # Check if user calling the function is a global owner (has permission id 1)
    if store['user_global_permission_level'][auth_user_index] != 1:
        raise AccessError(description='The authorised user is not a streams global owner')

    # Check if the u_id refers to a valid user
    if u_id not in store['user_id']:
        raise InputError(description='Not a valid user_id')

    u_id_index = store['user_id'].index(u_id)

    # Check if the person is trying to remove themselves as the last owner
    if store['user_global_permission_level'].count(1) == 1 and auth_user_index == u_id_index:
        raise InputError(description='Cannot remove only Streams owner')

    # Remove u_id from general members' id list
    store['user_id'].remove(u_id)
    store['deleted_u_ids'].append(u_id)
    email = store['user_emails'][u_id_index]

    # Delete email, password, first name, last name, handle and global permission
    del store['user_emails'][u_id_index]
    del store['user_passwords'][u_id_index]
    del store['user_first_names'][u_id_index]
    del store['user_last_names'][u_id_index]
    del store['user_handles'][u_id_index]
    del store['user_global_permission_level'][u_id_index]

    # Delete all their tokens
    for user_token in store['user_tokens']:
        if decode_jwt(user_token).get('username') == email:
            store['user_tokens'].remove(user_token)

    # Delete from channel
    for channel in store['channel_members_id']:
        if email in channel:
            channel_index = store['channel_members_id'].index(channel)
            email_index = channel.index(email)
            channel.remove(email)
            del store['channel_permissions'][channel_index][email_index]

    # Delete from DM
    for dm in store['dm_members_id']:
        if email in dm:
            dm.remove(email)

    # Modify messages in channels
    for channel in store['channel_messages']:
        for message in channel:
            if message.get('u_id') == u_id:
                message['message'] = "Removed user"

    # Modify messages in DMs
    for dm in store['dm_messages']:
        for message in dm:
            if message.get('u_id') == u_id:
                message['message'] = "Removed user"

    return {}
