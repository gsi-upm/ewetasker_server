from flask import Flask
from delivery.channels import *

app = Flask(__name__)

@app.route("/channels")
def channels():
    return get_channels()


if __name__ == '__main__':
    app.run(debug=True)