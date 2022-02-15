import sys

MESSAGE_LIST = []

def authorise(function):
    """
    You need a function here authorise which contains another function called wrapper.
    This wrapper function authenticates the token against CrocodileLikesStrawberries and if valid calls the function given as input,
    authorise then needs to return wrapper.
    """
def wrapper(auth_token, args, **kwargs):
    if auth_token != "CrocodileLikesStrawberries":
        raise Exception('Invalid token')
    return function(args, **kwargs)


@authorise
def get_messages():
    return MESSAGE_LIST

@authorise
def add_messages(msg):
    global MESSAGE_LIST
    MESSAGE_LIST.append(msg)

if __name__ == '__main__':
    auth_token = ""
    if len(sys.argv) == 2:
        auth_token = sys.argv[1]

    add_messages(auth_token, "Hello")
    add_messages(auth_token, "How")
    add_messages(auth_token, "Are")
    add_messages(auth_token, "You?")
    print(get_messages(auth_token))
