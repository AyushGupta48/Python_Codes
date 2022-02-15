import pytest

from src.auth import auth_login_v2, auth_register_v2
from src.error import InputError
import requests
from src.config import url

# Email address is not registered


def test_unassociated_email(clear_data):
    auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla")
    with pytest.raises(InputError):
        auth_login_v2("different@gmail.com", "abcdef")

# No email passed in


def test_no_email_entered(clear_data):
    auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla")
    with pytest.raises(InputError):
        auth_login_v2(None, "abcdef")

# Password does not match


def test_wrong_password(clear_data):
    auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla")
    with pytest.raises(InputError):
        auth_login_v2("valid@gmail.com", "randompassword")

# Wrong password (case sensitive)


def test_wrong_password_case_sensitive(clear_data):
    auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla")
    with pytest.raises(InputError):
        auth_login_v2("valid@gmail.com", "ABCDEF")

# No password passed in


def test_no_password_entered(clear_data):
    auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla")
    with pytest.raises(InputError):
        auth_login_v2("valid@gmail.com", None)


# Wrong password (someone elses' password)
def test_wrong_password_password_in_user_passwords(clear_data):
    auth_register_v2("unique@gmail.com", "differentpassword", "Please", "Work")
    auth_register_v2("stop@gmail.com", "strongpassword", "Whats", "Happening")
    with pytest.raises(InputError):
        auth_login_v2("unique@gmail.com", "strongpassword")


# Testing if user_ids are correctly assigned
def test_user_id(clear_data):
    auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla")
    auth_register_v2("new@gmail.com", "abcdef", "Dan", "Li")
    auth_register_v2("old@gmail.com", "abcdef", "Vikram", "Sun")
    auth_register_v2("original@gmail.com", "abcdef", "Ayush", "Gupt")
    auth_register_v2("unique@gmail.com", "differentpassword", "Please", "Work")
    auth_register_v2("stop@gmail.com", "strongpassword", "Whats", "Happening")

    assert(auth_login_v2("valid@gmail.com", "abcdef").get('auth_user_id') == 0)
    assert(auth_login_v2("new@gmail.com", "abcdef").get('auth_user_id') == 1)
    assert(auth_login_v2("old@gmail.com", "abcdef").get('auth_user_id') == 2)
    assert(auth_login_v2("original@gmail.com", "abcdef").get('auth_user_id') == 3)
    assert(auth_login_v2("stop@gmail.com",
           "strongpassword").get('auth_user_id') == 5)

# Testing if both auth_register and auth_login return the same user_ids


def test_compare_login_and_register(clear_data):
    assert(auth_register_v2("valid@gmail.com", "abcdef", "Pranav", "Mangla").get('auth_user_id')
           == auth_login_v2("valid@gmail.com", "abcdef").get('auth_user_id'))
    assert(auth_register_v2("qwert@gmail.com", "abcdef", "Pranav", "Mangla").get('auth_user_id')
           == auth_login_v2("qwert@gmail.com", "abcdef").get('auth_user_id'))

#################
# Below are the HTTP tests


def test_http_login(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response1 = requests.post(url + "auth/register/v2", json=payload1)
    response_data1 = response1.json()

    assert response_data1['auth_user_id'] == 0

    payload2 = {
        "email": "valid@gmail.com",
        "password": "aBc293"
    }
    response2 = requests.post(url + "auth/login/v2", json=payload2)
    response_data2 = response2.json()

    assert response_data2['auth_user_id'] == 0


def test_http_compare_login_and_register(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response1 = requests.post(url + "auth/register/v2", json=payload1)
    response_data1 = response1.json()

    payload2 = {
        "email": "valid@gmail.com",
        "password": "aBc293"
    }
    response2 = requests.post(url + "auth/login/v2", json=payload2)
    response_data2 = response2.json()

    assert response_data1.get(
        'auth_user_id') == response_data2.get('auth_user_id')


def test_http_multiple_users(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "abcdef",
        "name_first": "Pranav",
        "name_last": "Mangla"
    }
    response1 = requests.post(url + "auth/register/v2", json=payload1)
    response_data1 = response1.json()

    payload2 = {
        "email": "new@gmail.com",
        "password": "abcdef",
        "name_first": "Dan",
        "name_last": "Li"
    }
    response2 = requests.post(url + "auth/register/v2", json=payload2)
    response_data2 = response2.json()

    payload3 = {
        "email": "old@gmail.com",
        "password": "abcdef",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }

    response3 = requests.post(url + "auth/register/v2", json=payload3)
    response_data3 = response3.json()

    payload4 = {
        "email": "original@gmail.com",
        "password": "abcdef",
        "name_first": "Ayush",
        "name_last": "Gupt"
    }

    response4 = requests.post(url + "auth/register/v2", json=payload4)
    response_data4 = response4.json()

    payload5 = {
        "email": "unique@gmail.com",
        "password": "differentpassword",
        "name_first": "Please",
        "name_last": "Work"
    }

    requests.post(url + "auth/register/v2", json=payload5)

    payload6 = {
        "email": "stop@gmail.com",
        "password": "strongpassword",
        "name_first": "Whats",
        "name_last": "Happening"
    }

    response6 = requests.post(url + "auth/register/v2", json=payload6)
    response_data6 = response6.json()

    payload7 = {
        "email": "valid@gmail.com",
        "password": "abcdef"
    }
    response7 = requests.post(url + "auth/login/v2", json=payload7)
    response_data7 = response7.json()

    assert response_data1.get(
        'auth_user_id') == response_data7.get('auth_user_id')

    payload8 = {
        "email": "new@gmail.com",
        "password": "abcdef"
    }
    response8 = requests.post(url + "auth/login/v2", json=payload8)
    response_data8 = response8.json()

    assert response_data2.get(
        'auth_user_id') == response_data8.get('auth_user_id')

    payload9 = {
        "email": "old@gmail.com",
        "password": "abcdef"
    }
    response9 = requests.post(url + "auth/login/v2", json=payload9)
    response_data9 = response9.json()

    assert response_data3.get(
        'auth_user_id') == response_data9.get('auth_user_id')

    payload10 = {
        "email": "original@gmail.com",
        "password": "abcdef"
    }
    response10 = requests.post(url + "auth/login/v2", json=payload10)
    response_data10 = response10.json()

    assert response_data4.get(
        'auth_user_id') == response_data10.get('auth_user_id')

    payload11 = {
        "email": "stop@gmail.com",
        "password": "strongpassword"
    }
    response11 = requests.post(url + "auth/login/v2", json=payload11)
    response_data11 = response11.json()

    assert response_data6.get(
        'auth_user_id') == response_data11.get('auth_user_id')


def test_http_no_email(clear_data_http):

    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response1 = requests.post(url + "auth/register/v2", json=payload1)
    response_data1 = response1.json()

    assert response_data1['auth_user_id'] == 0

    payload2 = {
        "email": None,
        "password": "aBc293"
    }
    response2 = requests.post(url + "auth/login/v2", json=payload2)
    response_data2 = response2.json()

    assert response_data2.get('code') == 400


def test_http_wrong_email(clear_data_http):

    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response1 = requests.post(url + "auth/register/v2", json=payload1)
    response_data1 = response1.json()

    assert response_data1['auth_user_id'] == 0

    payload2 = {
        "email": "compeltelydifferenet@gmail.com",
        "password": "aBc293"
    }
    response2 = requests.post(url + "auth/login/v2", json=payload2)
    response_data2 = response2.json()

    assert response_data2.get('code') == 400


def test_http_wrong_password(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response1 = requests.post(url + "auth/register/v2", json=payload1)
    response_data1 = response1.json()

    assert response_data1['auth_user_id'] == 0

    payload2 = {
        "email": "valid@gmail.com",
        "password": "wrongpassword"
    }
    response2 = requests.post(url + "auth/login/v2", json=payload2)
    response_data2 = response2.json()

    assert response_data2.get('code') == 400


def test_http_no_password(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response1 = requests.post(url + "auth/register/v2", json=payload1)
    response_data1 = response1.json()

    assert response_data1['auth_user_id'] == 0

    payload2 = {
        "email": "valid@gmail.com",
        "password": None
    }
    response2 = requests.post(url + "auth/login/v2", json=payload2)
    response_data2 = response2.json()

    assert response_data2.get('code') == 400


def test_http_multiple_wrong_password(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    requests.post(url + "auth/register/v2", json=payload1).json()

    payload2 = {
        "email": "valid2@gmail.com",
        "password": "yeeticusmaximus",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    requests.post(url + "auth/register/v2", json=payload2)

    login_payload = {
        "email": "valid@gmail.com",
        "password": "yeeticusmaximus"
    }
    response_login = requests.post(
        url + "auth/login/v2", json=login_payload).json()
        
    assert response_login.get('code') == 400
