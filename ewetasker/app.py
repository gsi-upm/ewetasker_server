from flask import Flask
from delivery.channels import *
from flask_cors import CORS
from flask import request

app = Flask(__name__)
CORS(app)

@app.route("/channels")
def channels():
    return get_channels()

@app.route("/channels/import", methods = ['POST'])
def import_channel():
    re = request.get_json()
    return re["@id"]

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)