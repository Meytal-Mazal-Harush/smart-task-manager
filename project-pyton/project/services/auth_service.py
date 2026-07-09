import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
import bcrypt

# מפתח סודי פנימי של השרת לחיתום הטוקנים (במציאות שומרים אותו בקובץ env.)
SECRET_KEY = "SUPER_SECRET_KEY_DONT_TELL_ANYONE_12345!"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ---------------------------------------------------------
# 1. פונקציות לניהול והצפנת סיסמאות (Hashing)
# ---------------------------------------------------------
def hash_password(password: str) -> str:
    """הופך סיסמה גולמית ל-Hash מוצפן ומאובטח לבסיס הנתונים"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """בודק האם הסיסמה שהוזנה ב-Login מתאימה ל-Hash השמור ב-DB"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# ---------------------------------------------------------
# 2. פונקציה לייצור טוקן מאובטח (JWT) עבור המשתמש
# ---------------------------------------------------------
def create_access_token(data: dict) -> str:
    """מייצר טוקן חתום המכיל את ה-ID והתפקיד של המשתמש"""
    to_encode = data.copy()

    # הגדרת זמן תפוגה לטוקן
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # קידוד וחתימה על הטוקן באמצעות המפתח הסודי של השרת
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ---------------------------------------------------------
# 3. פונקציה לאימות ופענוח הטוקן (הגנה על ה-Routes)
# ---------------------------------------------------------
def verify_access_token(token: str):
    """מפענח את הטוקן, בודק שלא פג תוקפו ומחזיר את נתוני המשתמש"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # מחזיר מילון עם user_id ו-role
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again."
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid security token."
        )