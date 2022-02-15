import pytest
from json import dumps
from src.auth import auth_register_v2, auth_login_v2
from src.error import InputError
import requests
from src.config import url

# No @ sign in email


def test_register_invalid_email_no_at_sign(clear_data):
    with pytest.raises(InputError):
        auth_register_v2("aergaer.com", "aer127H", "Pranav", "Mangla")

# No . in email


def test_register_invalid_email_no_dot(clear_data):
    with pytest.raises(InputError):
        auth_register_v2("agiero@aigo", "aer127H", "Pranav", "Mangla")

# No . and no @ sign in email


def test_register_invalid_email_no_at_and_no_dot(clear_data):
    with pytest.raises(InputError):
        auth_register_v2("neirXXnfdf", "aer127H", "Pranav", "Mangla")

# Two @ signs in email


def test_register_invalid_email_two_at(clear_data):
    with pytest.raises(InputError):
        auth_register_v2("neirX@sad@Xnfdf", "aer127H", "Pranav", "Mangla")

# No email passed


def test_register_invalid_email_none(clear_data):
    with pytest.raises(InputError):
        auth_register_v2(None, "aer127H", "Pranav", "Mangla")

# Empty email passed


def test_register_invalid_email_empty(clear_data):
    with pytest.raises(InputError):
        auth_register_v2("", "aer127H", "Pranav", "Mangla")

# Duplicate Email


def test_register_duplicate_email(clear_data):
    auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li")
    with pytest.raises(InputError):
        auth_register_v2("valid@gmail.com", "aer127H", "Pranav", "Mangla")

# No password


def test_register_no_password(clear_data):
    with pytest.raises(InputError):
        auth_register_v2("valid@gmail.com", None, "Daniel", "Li")

# Password length < 6


def test_register_short_password(clear_data):
    with pytest.raises(InputError):
        auth_register_v2("valid@gmail.com", "abcde", "Daniel", "Li")

# No firstname


def test_register_no_firstname(clear_data):
    with pytest.raises(InputError):
        auth_register_v2("valid@gmail.com", "aBc293", None, "Li")

# Empty firstname


def test_register_empty_firstname(clear_data):
    with pytest.raises(InputError):
        auth_register_v2("valid@gmail.com", "aBc293", "", "Li")

# Firstname > 50


def test_register_long_firstname(clear_data):
    with pytest.raises(InputError):
        auth_register_v2("valid@gmail.com", "aBc293",
                         "WolfeschlegelsteinhausenbergerdorffWolfeschlegelsteinhausenbergerdorffWolfeschlegelsteinhausenbergerdorff", "Li")

# No lastname


def test_register_no_lastname(clear_data):
    with pytest.raises(InputError):
        auth_register_v2("valid@gmail.com", "aBc293", "Daniel", None)

# Empty lastname


def test_register_empty_lastname(clear_data):
    with pytest.raises(InputError):
        auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "")

# Lastname > 50


def test_register_long_lastname(clear_data):
    with pytest.raises(InputError):
        auth_register_v2("valid@gmail.com", "aBc293", "Daniel",
                         "WolfeschlegelsteinhausenbergerdorffWolfeschlegelsteinhausenbergerdorffWolfeschlegelsteinhausenbergerdorff")

# Test for user id


def test_user_id_correct(clear_data):
    auth_register_v2("valid@gmail.com", "aBc293", "Daniel", "Li")
    assert auth_login_v2("valid@gmail.com", "aBc293").get('auth_user_id') == 0

#################
# Below are the HTTP tests


def test_http_user_id(clear_data_http):
    payload = {
        "email": "valid@gmail.com",
        "password": "aBc293",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response = requests.post(f"{url}auth/register/v2", json=payload)
    response_data = response.json()

    assert response_data['auth_user_id'] == 0


def test_http_multiple(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "jdfnladsfa",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response1 = requests.post(f"{url}auth/register/v2", json=payload1)
    response_data1 = response1.json()

    assert response_data1['auth_user_id'] == 0

    payload2 = {
        "email": "valid2@gmail.com",
        "password": "alkdjnfklasd",
        "name_first": "Vikram",
        "name_last": "Sundar"
    }
    response2 = requests.post(f"{url}auth/register/v2", json=payload2)
    response_data2 = response2.json()

    assert response_data2['auth_user_id'] == 1

    payload3 = {
        "email": "valid3@gmail.com",
        "password": "aBc293",
        "name_first": "Pranav",
        "name_last": "Mangla"
    }
    response3 = requests.post(f"{url}auth/register/v2", json=payload3)
    response_data3 = response3.json()

    assert response_data3['auth_user_id'] == 2


def test_http_duplicate_email(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "jdfnladsfa",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response1 = requests.post(f"{url}auth/register/v2", json=payload1)
    response_data1 = response1.json()

    assert response_data1['auth_user_id'] == 0

    payload2 = {
        "email": "valid@gmail.com",
        "password": "jdfnladsfa",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response2 = requests.post(f"{url}auth/register/v2", json=payload2)
    response_data2 = response2.json()

    assert response_data2.get('code') == 400


def test_http_no_email(clear_data_http):
    payload1 = {
        "email": None,
        "password": "jdfnladsfa",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response1 = requests.post(f"{url}auth/register/v2", json=payload1)
    response_data1 = response1.json()

    assert response_data1.get('code') == 400


def test_http_invalid_email(clear_data_http):
    payload1 = {
        "email": "coolemail.com",
        "password": "jdfnladsfa",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response1 = requests.post(f"{url}auth/register/v2", json=payload1)
    response_data1 = response1.json()

    assert response_data1.get('code') == 400


def test_http_no_password(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": None,
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response1 = requests.post(f"{url}auth/register/v2", json=payload1)
    response_data1 = response1.json()

    assert response_data1.get('code') == 400


def test_http_short_password(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "small",
        "name_first": "Daniel",
        "name_last": "Li"
    }
    response1 = requests.post(f"{url}auth/register/v2", json=payload1)
    response_data1 = response1.json()

    assert response_data1.get('code') == 400


def test_http_no_first_name(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "validpassword",
        "name_first": "",
        "name_last": "Li"
    }
    response1 = requests.post(f"{url}auth/register/v2", json=payload1)
    response_data1 = response1.json()

    assert response_data1.get('code') == 400


def test_http_first_name_too_long(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "validpassword",
        "name_first": "thisisastringofmorethan50charactershopefullythistriggerstheinputerrorpelasework",
        "name_last": "Li"
    }
    response1 = requests.post(f"{url}auth/register/v2", json=payload1)
    response_data1 = response1.json()

    assert response_data1.get('code') == 400


def test_http_no_last_name(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "validpassword",
        "name_first": "Daniel",
        "name_last": ""
    }
    response1 = requests.post(f"{url}auth/register/v2", json=payload1)
    response_data1 = response1.json()

    assert response_data1.get('code') == 400


def test_http_last_name_too_long(clear_data_http):
    payload1 = {
        "email": "valid@gmail.com",
        "password": "validpassword",
        "name_first": "Daniel",
        "name_last": "thisisastringofmorethan50charactershopefullythistriggerstheinputerrorpelasework"
    }
    response1 = requests.post(f"{url}auth/register/v2", json=payload1)
    response_data1 = response1.json()
    
    assert response_data1.get('code') == 400
