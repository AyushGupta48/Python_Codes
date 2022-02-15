import pytest

from src.other import generate_jwt, decode_jwt


def test_generation_works():
    assert generate_jwt('minion', 0) == generate_jwt('minion', 0)


def test_decode_works():
    token = generate_jwt('minion', 0)
    assert decode_jwt(token) == decode_jwt(token)


def test_both_work():
    token = generate_jwt('minion', 0)
    print(decode_jwt(token))
    assert decode_jwt(token) == {'session_id': 0, 'username': 'minion'}
