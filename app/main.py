from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import dotenv_values
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers.household_router import router as household_router
from routers.book_router import router as book_router
from routers.address_router import router as address_router
from routers.users_router import router as user_router
<<<<<<< HEAD
from routers.authentication_router import router as auth_router
=======
from routers.comment_router import router as comment_router
>>>>>>> 023d65c2355c0d0a6698c7b8b398b5fbd6eeae91
from Imgur.Imgur import authenticate
from fastapi.middleware.cors import CORSMiddleware

config = dotenv_values(".env")

app = FastAPI()

origins = ["*"]

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
    # app.imgur_client = authenticate()


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(household_router, tags=["households"], prefix="/households")
app.include_router(book_router, tags=["bookings"], prefix="/bookings")
app.include_router(address_router, tags=["addresses"], prefix="/addresses")
app.include_router(user_router, tags=["users"], prefix="/users")
<<<<<<< HEAD
app.include_router(auth_router, tags=["auth"], prefix="/auth")
=======
app.include_router(comment_router, tags=["comments"], prefix="/comments")
>>>>>>> 023d65c2355c0d0a6698c7b8b398b5fbd6eeae91

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
