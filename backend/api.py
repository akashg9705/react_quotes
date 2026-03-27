from fastapi import FastAPI
from pydantic import BaseModel
from backend.db import add_subscriber, unsubscribe, get_all_subscribers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    email: str

@app.get("/")
def home():
    return {"message": "Quote SaaS API Running 🚀"}

@app.post("/subscribe")
def subscribe(data: EmailRequest):
    if add_subscriber(data.email):
        return {"status": "Subscribed 🎉"}
    return {"status": "Already exists"}

@app.post("/unsubscribe")
def remove(data: EmailRequest):
    unsubscribe(data.email)
    return {"status": "Unsubscribed"}

@app.get("/subscribers")
def subscribers():
    return {"data": get_all_subscribers()}