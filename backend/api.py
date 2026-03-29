from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from jose import jwt

from backend.auth import (
    hash_password,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)

from backend.db import (
    add_subscriber,
    unsubscribe,
    get_all_subscribers,
    create_user,
    get_user,
    init_db
)

from backend.quotes import get_quote

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    init_db()

# 🔐 AUTH SYSTEM
security = HTTPBearer()

def get_current_user(token=Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# 🌐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://react-quotes-ten.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 MODELS
class AuthRequest(BaseModel):
    email: str
    password: str

class SubscriberRequest(BaseModel):
    email: str

# 🏠 ROOT
@app.get("/")
def home():
    return {"message": "Quote SaaS API Running 🚀"}

# 💬 QUOTE OF THE DAY
@app.get("/quote")
def quote():
    try:
        text, author = get_quote()
        return {"quote": text, "author": author}
    except:
        return {"quote": "The best way to predict the future is to create it.", "author": "Peter Drucker"}

# 🔐 SIGNUP
@app.post("/signup")
def signup(data: AuthRequest):
    hashed = hash_password(data.password)

    if create_user(data.email, hashed):
        return {"status": "User created"}
    return {"status": "User already exists"}

# 🔐 LOGIN
@app.post("/login")
def login(data: AuthRequest):
    user = get_user(data.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id, email, hashed_password = user

    if not verify_password(data.password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"user_id": user_id})

    return {"access_token": token}

# 📬 SUBSCRIBE (PROTECTED)
@app.post("/subscribe")
def subscribe(
    data: SubscriberRequest,
    user_id=Depends(get_current_user)
):
    if add_subscriber(data.email, user_id):
        return {"status": "Subscribed"}
    return {"status": "Already exists"}

# ❌ UNSUBSCRIBE (PROTECTED)
@app.post("/unsubscribe")
def remove(
    data: SubscriberRequest,
    user_id=Depends(get_current_user)
):
    unsubscribe(data.email, user_id)
    return {"status": "Unsubscribed"}

# 📊 DASHBOARD (PROTECTED)
@app.get("/subscribers")
def subscribers(user_id=Depends(get_current_user)):
    return {"data": get_all_subscribers(user_id)}

# 📈 STATS (PROTECTED)
@app.get("/stats")
def stats(user_id=Depends(get_current_user)):
    subs = get_all_subscribers(user_id)
    total = len(subs)
    active = sum(1 for s in subs if s[1] == "active")
    inactive = total - active
    return {"total": total, "active": active, "inactive": inactive}