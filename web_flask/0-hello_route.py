#!/usr/bin/python3
"""starts the web app 

the app listens on 0.0.0.0, port 5000.
routes:
    /:Display 'Hello HBHB!'
"""
from flask import Flask

app = Flask(__name__)

@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Display 'Hello HBNB!'"""
    return ("Hello HBHB!")

if __name__ == "__main__":
    app.run(host="0.0.0.0")

