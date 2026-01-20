from fastapi import APIRouter, HTTPException
from backend.app.schemas.user import UserCreate
from backend.app.db.connection import get_connection
import psycopg2

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def create_user(user: UserCreate):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO pronounce.users (username)
            VALUES (%s)
            RETURNING id, username, created_at;
            """,
            (user.username,)
        )
        row = cur.fetchone()
        conn.commit()

        return {
            "id": row[0],
            "username": row[1],
            "created_at": row[2]
        }

    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=409, detail="Username already exists")

    finally:
        cur.close()
        conn.close()

@router.delete("/{user_id}")
def delete_user(user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            DELETE FROM pronounce.users
            WHERE id = %s
            RETURNING id;
            """,
            (user_id,)
        )

        row = cur.fetchone()
        if not row:
            conn.rollback()
            raise HTTPException(status_code=404, detail="User not found")

        conn.commit()
        return {"message": "User deleted successfully", "user_id": user_id}

    finally:
        cur.close()
        conn.close()
