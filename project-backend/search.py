from typing import Counter
from _pytest.python_api import raises
from src.error import InputError, AccessError
from src.data_store import data_store
from src.other import decode_jwt

def search_v1(token, query_str):

    '''
    search_v1 lets the user return a collection of messages in all of the channels/DMs 
    that the user has joined that contain the query

    Arguments:
        token      (string)   - Token of the user
        query_str  (integer)  - Query string to compare with messages


    Exceptions:
        InputError  -   Query string <= 0
                    -   Query string > 1000
                    
        AccessError -   Occurs when token is invalid
                    

    Return Value:
        messages list with relevant messages containing the query string
    '''

    store = data_store.get()

    messages_in_channel_and_dm = []   
    
    # Valid user id check
    if token not in store['user_tokens']:
        raise AccessError(description="Not a valid token")


    # Valid channel id check
    if len(query_str) < 1:
        raise InputError(description="Query string must be at least 1 character")

    # Valid user id check
    if len(query_str) > 1000:
        raise InputError(description="Query string must be less than 1000 characters")


    email = decode_jwt(token).get('username')
    # user_index = store['user_emails'].index(email)    
    # user_id = store['user_id'][user_index]            
    
    
    for channel in range(len(store['channel_members_id'])):
        if email in store['channel_members_id'][channel]:
            channel_index = channel

            for messages in range(len(store['channel_messages'][channel_index])):
                messages_in_channel_and_dm.append(store['channel_messages'][channel_index][messages].get("message"))
                  
    
    for dms in range(len(store['dm_members_id'])):
        if email in store['dm_members_id'][dms]:
            dm_index = dms

            for all_dms in range(len(store['dm_messages'][dm_index])):
                messages_in_channel_and_dm.append(store['dm_messages'][dm_index][all_dms].get("message"))      
    
    returned_messages = []
    
    for matches in range(len(messages_in_channel_and_dm)):
        if query_str in messages_in_channel_and_dm[matches]:
            returned_messages.append(messages_in_channel_and_dm[matches]) 
        
        matches += 1        

    data_store.set(store)
    
    return {
        "messages": returned_messages
    }
