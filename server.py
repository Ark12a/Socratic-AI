import os
import psycopg2
import bcrypt
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from livekit.api import AccessToken, VideoGrants
from dotenv import load_dotenv

# Environment variables load karein
load_dotenv()

app = FastAPI()

# Frontend (HTML) ko API call karne ki permission dena
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATABASE CONNECTION HELPER ---
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="tutor_db",
        user="postgres",
        password="1234" # Yahan apna password dalein
    )

# --- PYDANTIC MODELS ---
class UserAuth(BaseModel):
    email: str
    password: str

# ==========================================
# 1. LIVEKIT ROUTE (WebRTC Token)
# ==========================================
@app.get("/get-token")
def get_token(room_name: str = "ai-tutor-room", participant_name: str = "student"):
    # LiveKit Cloud room ke liye access permissions set karna
    grant = VideoGrants(room_join=True, room=room_name)
    
    # Naye builder pattern ke sath secure token generate karna
    token = (
        AccessToken(os.getenv("LIVEKIT_API_KEY"), os.getenv("LIVEKIT_API_SECRET"))
        .with_identity(participant_name)
        .with_name(participant_name)
        .with_grants(grant)
        .to_jwt()
    )
    
    return {"token": token}


# ==========================================
# 2. AUTHENTICATION ROUTES (PostgreSQL)
# ==========================================
@app.post("/register")
def register_user(user: UserAuth):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Password ko secure hash mein convert karna
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        cur.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
            (user.email, hashed_password.decode('utf-8'))
        )
        conn.commit()
        return {"message": "User registered successfully!"}
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    finally:
        cur.close()
        conn.close()

@app.post("/login")
def login_user(user: UserAuth):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT password_hash, session_count FROM users WHERE email = %s", (user.email,))
    result = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if result:
        stored_hash = result[0]
        session_count = result[1]
        
        if bcrypt.checkpw(user.password.encode('utf-8'), stored_hash.encode('utf-8')):
            return {
                "message": "Login successful", 
                "session_count": session_count,
                "status": "success"
            }
            
    raise HTTPException(status_code=401, detail="Invalid email or password")