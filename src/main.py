from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
import os
from fastapi.security import OAuth2PasswordBearer

from api.routes import users

load_dotenv()

app = FastAPI()
app.include_router(users.router)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST"),port=int(os.getenv("PORT")))