from re import A
import sys
import signal
from json import dumps
from _pytest.python_api import ApproxBase
from flask import Flask, request
import requests
from flask_cors import CORS
import threading
import time
from src import config
from src.config import url
from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1, auth_password_reset, auth_password_request_reset
from src.other import clear_v1
from src.channel import channel_join_v2, channel_messages_v2, channel_invite_v2, channel_addowner_v1, channel_removeowner_v1, channel_details_v2, channel_leave_v1
from src.channels import channels_create_v2, channels_list_v2, channels_listall_v2
from src.user_users import users_all_v1, user_profile_v1, user_setname_v1, user_setemail_v1, user_sethandle_v1
from src.admin import admin_userpermission_change_v1, admin_userremove_v1
from src.data_store import data_store
from src.message import message_send_v1, message_edit_v1, message_remove_v1, message_senddm_v1, message_send_later_channel, message_send_later_dm, message_react_v1, message_unreact_v1, send_message_if_time_come, message_pin_v1, message_unpin_v1, message_share_v1
from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1, dm_details_v1, dm_leave_v1, dm_messages_v1
from src.search import search_v1
from src.standup import standup_start, standup_active, standup_send

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

# Example
# @APP.route("/echo", methods=['GET'])
# def echo():
#     data = request.args.get('data')
#     if data == 'echo':
#    	    raise InputError(description='Cannot echo "echo"')
#     return dumps({
#         'data': data
#     })


@APP.route("/view", methods=['GET'])
def view():
    send_message_if_time_come()
    store = data_store.get()
    return dumps(store)

# Clear function call on http level


@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    send_message_if_time_come()
    clear_v1()
    return dumps({})

# Register function call on http level


@APP.route("/auth/register/v2", methods=['POST'])
def auth_register():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(auth_register_v2(
        request_data["email"],
        request_data["password"],
        request_data["name_first"],
        request_data["name_last"]
        )
        )

# Login function call on http level


@APP.route("/auth/login/v2", methods=['POST'])
def auth_login():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(auth_login_v2(
        request_data['email'],
        request_data['password'])
        )

#Logout function call on http level


@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(auth_logout_v1(
        request_data['token'])
    )

# Password Reset Request

@APP.route("/auth/passwordreset/request/v1", methods=["POST"])
def auth_request_password():
    request_data = request.get_json()
    send_message_if_time_come()
    auth_password_request_reset(request_data['email'])
    return dumps({})

# Password reset code entry

@APP.route("/auth/passwordreset/reset/v1", methods=["POST"])
def auth_reset_password():
    request_data = request.get_json()
    send_message_if_time_come()
    auth_password_reset(request_data['reset_code'], request_data['new_password'])
    return dumps({})

# Create function call on http level


@APP.route("/channels/create/v2", methods=['POST'])
def channel_create():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(channels_create_v2(
        request_data['token'],
        request_data['name'],
        request_data['is_public']
    ))

# List function call on http level


@APP.route("/channels/list/v2", methods=['GET'])
def channels_list():
    request_data = request.args.get('token')
    send_message_if_time_come()
    return dumps(channels_list_v2(request_data))


@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(channel_invite_v2(
        request_data['token'],
        request_data['channel_id'],
        request_data['u_id']
    ))


@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(channel_join_v2(
        request_data['token'],
        request_data['channel_id']
    ))


@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(channel_addowner_v1(
        request_data['token'],
        request_data['channel_id'],
        request_data['u_id']
    ))


@APP.route("/channel/removeowner/v1", methods=['POST'])
def channel_removeowner():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(channel_removeowner_v1(
        request_data['token'],
        request_data['channel_id'],
        request_data['u_id']
    ))


@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(channel_leave_v1(
        request_data['token'],
        request_data['channel_id']
    ))


@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    request_token = request.args.get('token')
    send_message_if_time_come()
    request_channel_id = request.args.get('channel_id')
    return dumps(channel_details_v2(
        request_token,
        int(request_channel_id)
    ))

# Listall function call on http level


@APP.route("/channels/listall/v2", methods=['GET'])
def channels_listall():
    request_data = request.args.get('token')
    send_message_if_time_come()
    return dumps(channels_listall_v2(request_data))

# Users all function call on http level


@APP.route("/users/all/v1", methods=['GET'])
def users_all():
    request_data = request.args.get('token')
    send_message_if_time_come()
    return dumps(users_all_v1(request_data))

# User profile function call on http level


@APP.route("/user/profile/v1", methods=['GET'])
def user_profile():
    request_token = request.args.get('token')
    send_message_if_time_come()
    request_u_id = request.args.get("u_id")
    return dumps(user_profile_v1(str(request_token), int(request_u_id)))

# User setname function call on http level


@APP.route("/user/profile/setname/v1", methods=['PUT'])
def user_setname():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(user_setname_v1(request_data["token"], request_data["name_first"], request_data["name_last"]))

# User setemail function call on http level


@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def user_setemail():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(user_setemail_v1(request_data["token"], request_data["email"]))

# User sethandle function call on http level


@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def user_sethandle():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(user_sethandle_v1(request_data["token"], request_data["handle_str"]))

# Channel messages function call on http level


@APP.route("/channel/messages/v2", methods=['GET'])
def channel_messages():
    request_token = request.args.get('token')
    send_message_if_time_come()
    request_channel_id = request.args.get('channel_id')
    request_start = request.args.get('start')
    return dumps(channel_messages_v2(str(request_token), int(request_channel_id), int(request_start)))

# Message send function call on http level


@APP.route("/message/send/v1", methods=['POST'])
def message_send():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(message_send_v1(request_data["token"], request_data["channel_id"], request_data["message"]))

# Message edit function call on http level


@APP.route("/message/edit/v1", methods=['PUT'])
def message_edit():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(message_edit_v1(request_data["token"], request_data["message_id"], request_data["message"]))

# Message remove function call on http level


@APP.route("/message/remove/v1", methods=['DELETE'])
def message_remove():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(message_remove_v1(request_data["token"], request_data["message_id"]))

# Message share 

@APP.route("/message/share/v1", methods=['POST'])
def message_share():
    request_data = request.get_json()
    return dumps(message_share_v1(request_data["token"], request_data["og_message_id"], request_data["message"], request_data["channel_id"], request_data["dm_id"]))

# DM create function call on http level


@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(dm_create_v1(request_data["token"], request_data["u_ids"]))

# DM list function call on http level


@APP.route("/dm/list/v1", methods=['GET'])
def dm_list():
    request_token = request.args.get('token')
    send_message_if_time_come()
    return dumps(dm_list_v1(request_token))

# DM remove function call on http level


@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(dm_remove_v1(request_data["token"], request_data["dm_id"]))

# DM details function call on http level


@APP.route("/dm/details/v1", methods=['GET'])
def dm_details():
    request_token = request.args.get('token')
    send_message_if_time_come()
    request_dm_id = int(request.args.get('dm_id'))
    return dumps(dm_details_v1(request_token, request_dm_id))

# DM leave function call on http level


@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(dm_leave_v1(request_data["token"], request_data["dm_id"]))

# DM messages function call on http level


@APP.route("/dm/messages/v1", methods=['GET'])
def dm_messages():
    request_token = request.args.get('token')
    send_message_if_time_come()
    request_dm_id = int(request.args.get('dm_id'))
    request_start = int(request.args.get('start'))
    return dumps(dm_messages_v1(request_token, request_dm_id, request_start))

# Send DM function call on http level


@APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(message_senddm_v1(request_data["token"], request_data["dm_id"], request_data["message"]))


@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission_change():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(admin_userpermission_change_v1(
        request_data['token'],
        request_data['u_id'],
        request_data['permission_id']
    ))


@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_userremove():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(admin_userremove_v1(request_data["token"], request_data['u_id']))

@APP.route("/search/v1", methods=['GET'])
def search():
    
    request_token = request.args.get("token")
    request_query_str = request.args.get("query_str")
    return dumps(search_v1(
        str(request_token), str(request_query_str)
    ))

#### NO NEED TO MODIFY BELOW THIS POINT

@APP.route("/message/react/v1", methods=['POST'])
def message_react():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(message_react_v1(
        request_data['token'],
        request_data['message_id'],
        request_data['react_id']
    ))

@APP.route("/message/unreact/v1", methods=['POST'])
def message_unreact():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(message_unreact_v1(
        request_data['token'],
        request_data['message_id'],
        request_data['react_id']
    ))


@APP.route("/message/sendlater/v1", methods=['POST'])
def message_sendlater():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(message_send_later_channel(request_data["token"], request_data["channel_id"], request_data["message"], request_data["time_sent"]))


@APP.route("/message/sendlaterdm/v1", methods=['POST'])
def message_sendlaterdm():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(message_send_later_dm(request_data["token"], request_data["dm_id"], request_data["message"], request_data["time_sent"]))

@APP.route("/standup/start/v1", methods=['POST'])
def standup_start_server():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(standup_start(request_data['token'], request_data['channel_id'], request_data['length']))

@APP.route("/standup/active/v1", methods=['GET'])
def standup_active_server():
    request_token = request.args.get('token')
    send_message_if_time_come()
    request_channel_id = int(request.args.get('channel_id'))
    return dumps(standup_active(request_token, request_channel_id))

@APP.route("/standup/send/v1", methods=['POST'])
def standup_send_server():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(standup_send(request_data['token'], request_data['channel_id'], request_data['message']))

@APP.route("/message/pin/v1", methods=['POST'])
def message_pin():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(message_pin_v1(
        request_data['token'],
        request_data['message_id']        
    ))

@APP.route("/message/unpin/v1", methods=['POST'])
def message_unpin():
    request_data = request.get_json()
    send_message_if_time_come()
    return dumps(message_unpin_v1(
        request_data['token'],
        request_data['message_id']        
    ))




#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)  # For coverage
    APP.run(port=config.port)  # Do not edit this port
