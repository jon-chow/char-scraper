"""Main router for the server.

Author: jon-chow
Created: 2023-06-13
Last Modified: 2023-06-13
"""

import json
import uvicorn
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from main import genshin_scraper


# ---------------------------------------------------------------------------- #
#                                     SETUP                                    #
# ---------------------------------------------------------------------------- #
app = fastapi.FastAPI()

origins = [
  "http://localhost:3000",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

class RunParams(BaseModel):
  function: str = ""
  category: str | None = ""
  folders: list | None = []


# ---------------------------------------------------------------------------- #
#                                    ROUTES                                    #
# ---------------------------------------------------------------------------- #

@app.get('/')
def hello_world():
  """Main route."""
  return 'Hello, World!'


@app.post('/run')
async def run(body: RunParams):
  """
  Runs the scraper with the specified parameters.
  POST /run
  """
  try:
    # Get parameters.
    function = "" if body.function is None else body.function
    category = "" if body.category is None else body.category
    folders = [] if body.folders is None else body.folders
    
    genshin_scraper(function=function, category=category, folders=folders)
  except Exception as e:
    return {
      "status": "error",
      "message": str(e),
    }
  
  return {
    "status": "success",
    "message": "Successfully ran scraper.",
  }


if __name__ == '__main__':
  uvicorn.run(
    "server:app",
    host="localhost",
    port=3001,
    reload=True,
  )
