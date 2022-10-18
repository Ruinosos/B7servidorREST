from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from dotenv import dotenv_values
from typing import List

import uvicorn

from model import Household

router = APIRouter()