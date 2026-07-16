"""
auth.py
User Registration & Login
"""

import uuid

from passlib.context import CryptContext

from database import get_mysql_connection

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)


def register_user(username, email, password):

    conn = get_mysql_connection()
    cursor = conn.cursor()

    # Check existing user
    cursor.execute(
        "SELECT * FROM users WHERE username=%s OR email=%s",
        (username, email)
    )

    user = cursor.fetchone()

    if user:
        cursor.close()
        conn.close()
        return {
            "success": False,
            "message": "User already exists"
        }

    user_id = str(uuid.uuid4())

    cursor.execute(
        """
        INSERT INTO users
        (id,username,email,password)
        VALUES(%s,%s,%s,%s)
        """,
        (
            user_id,
            username,
            email,
            hash_password(password)
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "success": True,
        "user_id": user_id
    }


def login_user(email, password):

    conn = get_mysql_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    if not verify_password(password, user["password"]):
        return {
            "success": False,
            "message": "Invalid password"
        }

    return {
        "success": True,
        "user_id": user["id"],
        "username": user["username"],
        "email": user["email"]
    }