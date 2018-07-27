from flask import Flask
from delivery.channels import get_base_channels, get_custom_channels, get_custom_category_channels, get_category_channels, get_subchannels_of_channel, import_new_channel, delete_custom_channel_with_uri
from delivery.rules import create_rule
from flask_cors import CORS
from flask import request
from data.database.users import *

app = Flask(__name__)
CORS(app)

@app.route("/channels/base")
def base_channels():
    return get_base_channels()

@app.route("/channels/custom")
def custom_channels():
    return get_custom_channels()

@app.route("/channels/custom/category/<path:uri>")
def custom_category_channels(uri):
    return get_custom_category_channels(uri)

@app.route("/channels/category/<path:uri>")
def category_channels(uri):
    return get_category_channels(uri)

@app.route("/channels/custom/base_channel/<path:uri>")
def subchannels_of_channel(uri):
    return get_subchannels_of_channel(uri)

@app.route("/channels/import", methods = ['POST'])
def import_channel():
    channel = request.get_json()
    return import_new_channel(channel)

@app.route("/channels/custom/delete/<path:uri>", methods = ['DELETE'])
def delete_custom_channel(uri):
    return delete_custom_channel_with_uri(uri)

#@app.route("/rules")
#def base_rules():
#    return get_base_channels()
@app.route("/rules/new", methods = ['POST'])
def post_create_rule():
    rule = request.get_json()
    return create_rule(rule)

@app.route("/users/new", methods=['POST'])
def new_user():
    username = request.form.get('username')
    password= request.form.get('password')
    return create_user(username, password)

@app.route("/users/login", methods=['POST'])
def login():
    username = request.form.get('username')
    password= request.form.get('password')
    return login_user(username, password)

@app.route("/users/delete", methods=['POST'])
def delete_user():
    username = request.form.get('username')
    password= request.form.get('password')
    return remove_user(username, password)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
