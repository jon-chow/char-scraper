"""Main router for the server.

Author: jon-chow
Created: 2023-06-13
Last Modified: 2023-06-13
"""

import flask
import json
from flask_cors import CORS

from main import genshin_scraper


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


# @app.route('/data', methods=['GET'])
# def data():
#   """
#   Returns the data from the JSON files.
#   GET /data
#   """
#   with open("data/chars.json", "r") as f:
#     data = json.load(f)
#   return flask.jsonify(data)


@app.route('/run', methods=['POST'])
def run():
  """
  Runs the scraper with the specified parameters.
  POST /run
  """
  try:
    data = flask.request.get_json()
    
    # Get parameters.
    function = "" if "function" not in data else data["function"]
    category = "" if "category" not in data else data["category"]
    folders = [] if "folders" not in data else data["folders"]
    
    genshin_scraper(function=function, category=category, folders=folders)
  except Exception as e:
    return flask.jsonify({"success": False, "error": str(e)})
  
  return flask.jsonify({"success": True})


if __name__ == '__main__':
  app.run("localhost", 3001, threaded=True, debug=True)
