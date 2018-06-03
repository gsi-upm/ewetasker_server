from flask import Flask
from delivery.channels import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/channels")
def channels():
    return get_channels()


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)