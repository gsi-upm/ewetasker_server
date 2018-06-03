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

@app.route("/channels/import", methods = ['POST'])
def import_channel():
    channel = request.get_json()
    return import_new_channel(channel)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)