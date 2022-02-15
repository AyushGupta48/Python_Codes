from _pytest.python_api import raises
from src.error import InputError, AccessError
from src.data_store import data_store
from src.other import decode_jwt, generate_jwt
import re


def users_all_v1(token):
    '''
    Users_all_v1 lists all the users currently registered in the data store.

    Arguments:
        token      (string)   - Token of user

    Exceptions:
        AccessError  -   Occurs when the token is invalid

    Return Value:
        Returns a dictionary {'users': []} where the list contains a dictionary for each registered member
    '''
    store = data_store.get()

    # Valid token check
    if token not in store['user_tokens']:
        raise AccessError(description="Not a valid token")

    to_return_values = []

    # User an id_counter to iterate and add the id of each user
    id_counter = 0
    for email in store['user_emails']:

        # Add items to the dictionary
        dictionary = {
            "u_id": id_counter,
            "email": email,
            "name_first": store['user_first_names'][id_counter],
            "name_last": store['user_last_names'][id_counter],
            "handle_str": store['user_handles'][id_counter]
        }

        # Append to the list we want to return
        to_return_values.append(dictionary)

        # Increment the id counter to move onto next person
        id_counter += 1

    return {
        "users": to_return_values
    }


def user_profile_v1(token, u_id):
    '''
    User_profile_v1 returns the information of a specified user

    Arguments:
        token      (string)     - Token of user
        u_id       (int)        - User id of user info to return


    Exceptions:
        InputError  -   Occurs when user id passed in doesn't exist

        AccessError -   Occurs when token is invalid

    Return Value:
        Returns a dictionary containing the user's id, email, first name, last name and handle
    '''
    store = data_store.get()

    # Valid token check
    if token not in store['user_tokens']:
        raise AccessError(description="Not a valid token")

    # Check if user has been deleted
    if u_id in store['deleted_u_ids']:
        return {
            "u_id": u_id,
            "email": "",
            "name_first": "Removed",
            "name_last": "user",
            "handle_str": ""
        }

    # Check if the u_id asked for actually exists
    if u_id not in store['user_id']:
        raise InputError(description='Not a valid u_id')

    return {
        "user": {
                "u_id": u_id,
                "email": store['user_emails'][u_id],
                "name_first": store['user_first_names'][u_id],
                "name_last": store['user_last_names'][u_id],
                "handle_str": store['user_handles'][u_id]
        }
    }


def user_setname_v1(token, name_first, name_last):
    '''
    User_setname_v1 changes the first and last names of the user whose token was passed in.

    Arguments:
        token      (string)   - Token of user
        name_first (string)   - First name user wants to change to
        name_last  (string)   - Last name user wants to change to

    Exceptions:
        InputError  -   Occurs when no first name is given/first name is empty
                    -   Occurs when first name is longer than 50 characters
                    -   Occurs when no last name is given/last name is empty
                    -   Occurs when last name is longer than 50 characters\

        AccessError -   Occurs when token is invalid

    Return Value:
        No Return
    '''
    store = data_store.get()

    # Valid token check
    if token not in store['user_tokens']:
        raise AccessError(description="Not a valid token")

    # First name checks
    if name_first is None or name_first == "":
        raise InputError(description="Invalid first name: no first name given")

    if len(name_first) > 50:
        raise InputError(
            description="Invalid first name: first name is longer than 50 characters")

    # Last name checks
    if name_last is None or name_last == "":
        raise InputError(description="Invalid last name: no last name given")

    if len(name_last) > 50:
        raise InputError(
            description="Invalid last name: last name is longer than 50 characters")

    email = decode_jwt(token).get('username')

    # Getting the user id so we can update correct name
    idx = store['user_emails'].index(email)

    # Update names
    store['user_first_names'][idx] = name_first
    store['user_last_names'][idx] = name_last

    data_store.set(store)

    return {}


def user_setemail_v1(token, email):
    '''
    User_setemail_v1 changes the email address of the user whose token was passed in.

    Arguments:
        token      (string)   - Token of user
        email      (string)   - Email the user wants to change to

    Exceptions:
        InputError  -   Occurs when email is empty
                    -   Occurs when email is invalid
                    -   Occurs when email is already registered

        AccessError -   Occurs when token is invalid

    Return Value:
        No Return
    '''
    store = data_store.get()

    # Valid token check
    if token not in store['user_tokens']:
        raise AccessError(description="Not a valid token")

    # Email checks
    if email == None or len(email) == 0:
        raise InputError(description="Invalid email: no email given")

    # Valid email check
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(email_regex, email)):
        pass
    else:
        raise InputError(description="Invalid email")

    # Check to see if email is already used
    if email in store['user_emails']:
        raise InputError(description="Email is already used")

    # Start to replace all occurrences of email
    idx = store['user_emails'].index(decode_jwt(token).get('username'))

    store['user_emails'][idx] = email

    # Generate new valid token but keep the old one valid as well
    new_token = generate_jwt(email, decode_jwt(token).get('session_id'))
    store['user_tokens'].append(new_token)

    for channel in store['channel_members_id']:
        if decode_jwt(token).get('username') in channel:
            index = channel.index(decode_jwt(token).get('username'))
            channel[index] = email

    data_store.set(store)
    return {}


def user_sethandle_v1(token, handle_str):
    '''
    User_sethandle_v1 changes the handle of the user whose token was passed in.

    Arguments:
        token      (string)   - Token of user
        handle_str (string)   - Handle the user wants to change to

    Exceptions:
        InputError  -   Occurs when handle_str is shorter than three characters
                    -   Occurs when handle_str is longer than 20 characters
                    -   Occurs when handle_str contains non-alphanumeric characters
                    -   Occurs when handle_str is already being used

        AccessError -   Occurs when token is invalid

    Return Value:
        No Return
    '''
    store = data_store.get()

    # Valid token check
    if token not in store['user_tokens']:
        raise AccessError(description="Not a valid token")

    # Handle checks
    if len(handle_str) < 3:
        raise InputError(description="Handle is too short")

    if len(handle_str) > 20:
        raise InputError(description="Handle is too long")

    if not handle_str.isalnum():
        raise InputError(
            description="Handle contains non-alphanumeric characters")

    if handle_str in store['user_handles']:
        raise InputError(description="Handle is already used")

    # Now we can change the handle of the user
    # First get user id
    idx = store['user_emails'].index(decode_jwt(token).get('username'))

    # Now replace handle in handle list
    store['user_handles'][idx] = handle_str

    data_store.set(store)
    return {}
