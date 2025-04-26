import os
from dotenv import load_dotenv

load_dotenv()


import uvicorn
from fastapi import FastAPI, Response
from app.api import user, account, employee, auth, exchange, credit
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


app = FastAPI(title="Bank API Gateway", version="1.0.0")


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


app.include_router(user.router)
app.include_router(account.router)
app.include_router(employee.router)
app.include_router(auth.router)
app.include_router(exchange.router)
app.include_router(credit.router)

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
