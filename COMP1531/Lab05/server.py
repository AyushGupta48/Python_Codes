from json import dumps
from flask import Flask, request
from flask_cors import CORS

APP = Flask(__name__)
CORS(APP)

name_data = {
                'name': []  
            }

@APP.route("/name/add", methods=['POST'])
def add_name():
    added_name = request.form.get('name')
    name_data['name'].append(added_name)   


@APP.route("/names", methods=['GET'])
def list_all_names():
    return dumps(name_data)


@APP.route("/name/remove", methods=['DELETE'])
def remove_name():
    name_removed = request.form.get('name')
    name_data['name'].remove(name_removed)


@APP.route("/names/clear", methods=['DELETE'])
def clear_all_names():
    name_data['name'].clear() 


if __name__ == '__main__':
    APP.run()
