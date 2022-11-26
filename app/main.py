from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import dotenv_values
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers.household_router import router as household_router
from routers.book_router import router as book_router
from routers.address_router import router as address_router
from routers.users_router import router as user_router
from Imgur.Imgur import authenticate
from fastapi.middleware.cors import CORSMiddleware

config = dotenv_values(".env")

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")
    # app.imgur_client = authenticate()

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(household_router, tags=["households"], prefix="/households")
app.include_router(book_router, tags=["bookings"], prefix="/bookings")
app.include_router(address_router, tags=["addresses"], prefix="/addresses")
app.include_router(user_router, tags=["users"], prefix="/users")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
