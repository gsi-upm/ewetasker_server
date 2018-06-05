from flask import Flask
from delivery.channels import *
from flask_cors import CORS
from flask import request

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

@app.route("/channels/import", methods = ['POST'])
def import_channel():
    channel = request.get_json()
    return import_new_channel(channel)

@app.route("/channels/custom/delete/<path:uri>", methods = ['DELETE'])
def delete_custom_channel(uri):
    return delete_custom_channel_with_uri(uri)

if __name__ == '__main__':
    app.run(host="localhost", debug=True)