from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from db import get_connection
import bcrypt

router = APIRouter()


class UserCreate(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
def signup(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(user.password.encode("utf-8"), salt)

    # Store user
    cursor.execute(
        "INSERT INTO users (email, hashed_password) VALUES (%s, %s)",
        (user.email, hashed.decode("utf-8"))
    )
    conn.commit()
    conn.close()

    return {"message": "User created successfully"}
