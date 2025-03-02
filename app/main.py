import os
from dotenv import load_dotenv

load_dotenv()


import uvicorn
from fastapi import FastAPI
from app.api import user, account
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Bank API Gateway", version="1.0.0")

app.include_router(user.router)
app.include_router(account.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=os.environ['SERVER_HOST'], port=int(os.environ['SERVER_PORT']), reload=True)
