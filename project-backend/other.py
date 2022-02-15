from src.data_store import data_store
import jwt
import hashlib
import requests
from src.config import url
import smtplib
import os


SECRET = 'PRANAVMANGLAAYUSHGUPTACHRISSHIDANIELLIVIKRAMSUNDAR'

# Generates a new session id for jwt generation


def generate_new_session_id():
    store = data_store.get()
    SESSION_TRACKER = store['session_tracker']
    SESSION_TRACKER += 1
    store['session_tracker'] = SESSION_TRACKER
    data_store.set(store)
    return SESSION_TRACKER

# Clears all lists in the data store


def clear_v1():
    store = data_store.get()
    store['user_emails'] = []
    store['user_passwords'] = []
    store['user_first_names'] = []
    store['user_last_names'] = []
    store['user_handles'] = []
    store['user_id'] = []
    # store['user_sessions'] = []
    store['user_tokens'] = []
    store['user_global_permission_level'] = []
    store['user_reset_codes'] = []

    store['channel_id'] = []
    store['channel_names'] = []
    store['channel_is_public'] = []
    store['channel_members_id'] = []
    store['channel_messages'] = []
    store['channel_permissions'] = []

    store['dm_id'] = []
    store['dm_names'] = []
    store['dm_members_id'] = []
    store['dm_messages'] = []

    store['session_tracker'] = -1
    store['message_tracker'] = -1
    store['deleted_u_ids'] = []
    store['standup_tracker'] = -1
    store['standup_queue'] = []

    store['message_send_queue'] = []
    
    data_store.set(store)

    if os.path.exists("datastore.pkl"):
        os.remove("datastore.pkl")

# Encrypts password with sha256 algorithm


def encrypt(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Generates a jwt using the email and session id generated


def generate_jwt(username, session_id):
    return jwt.encode({'username': username, 'session_id': session_id}, SECRET, algorithm='HS256')

# Decodes the jwt


def decode_jwt(encoded_jwt):
    return jwt.decode(encoded_jwt, SECRET, algorithms=['HS256'])

def send_password_reset_code(email, reset_code):
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login('1531teamdodo@gmail.com','1531dodo')
    mail.sendmail('teamdodo1531@gmail.com', email, reset_code)
    mail.close
    return
