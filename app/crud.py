from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash

from app import models, schemas

password_hash = PasswordHash.recommended()


# Add a new user
def create_user(db: Session, user: schemas.UserCreate):

    hashed_password = password_hash.hash(user.password)

    db_user = models.User(
        email=user.email,
        username=user.username,
        password_hash=hashed_password
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    except IntegrityError:
        db.rollback()
        raise ValueError("Email or username already exists")


# Get user by ID
def get_user(db: Session, user_id: int):

    return db.query(models.User).filter(
        models.User.id == user_id
    ).first()

def get_user_by_username(db: Session, username: str):

    return db.query(models.User).filter(
        models.User.username == username
    ).first()