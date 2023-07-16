"""Main router for the server.

Author: jon-chow
Created: 2023-06-13
Last Modified: 2023-07-15
"""

import json
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from pydantic import BaseModel

from main import genshin_scraper
from utils.scrapers import get_all_names


# ---------------------------------------------------------------------------- #
#                                     SETUP                                    #
# ---------------------------------------------------------------------------- #

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.title = "Genshin JSON Data Generator API"
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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

class GetParams(BaseModel):
  category: str | None = ""

class RunParams(BaseModel):
  function: str = ""
  category: str | None = ""
  folders: list | None = []


# ---------------------------------------------------------------------------- #
#                                    ROUTES                                    #
# ---------------------------------------------------------------------------- #

@app.post('/get')
@limiter.limit("1/second")
async def get(request: Request, body: GetParams):
  """
  Gets the data from the specified category.
  POST /get
  """
  data = []
  try:
    # Get parameters.
    category = "" if body.category is None else body.category
    
    data = get_all_names(category=category) if category != "" else []
  except Exception as e:
    return {
      "status": "error",
      "message": str(e),
    }
  
  return {
    "status": "success",
    "message": data,
  }


@app.post('/run')
@limiter.limit("1/second")
async def run(request: Request, body: RunParams):
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
