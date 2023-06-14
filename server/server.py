"""Main router for the server.

Author: jon-chow
Created: 2023-06-13
Last Modified: 2023-06-13
"""

import flask
import json
from flask_cors import CORS

# Setup Flask app.
app = flask.Flask(__name__)
CORS(app)

# ---------------------------------------------------------------------------- #
#                                    ROUTES                                    #
# ---------------------------------------------------------------------------- #

@app.route('/')
def hello_world():
  """Main route."""
  return 'Hello, World!'


@app.route('/chars', methods=['GET'])
def chars():
  """
  Returns all characters.
  GET /chars
  """
  with open("data/chars.json", "r") as f:
    chars = json.load(f)
    return chars


if __name__ == '__main__':
  app.run("localhost", 3001, threaded=True)