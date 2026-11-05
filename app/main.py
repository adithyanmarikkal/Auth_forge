from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.security import verify_password, create_access_token
from app.database import get_db
from app import crud, schemas
from app.dependencies import get_current_user
app = FastAPI()


@app.get("/")
def home():
    return {"message": "Authentication API is running"}


# Add user
@app.post("/users", response_model=schemas.UserResponse, status_code=201)
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    try:
        return crud.create_user(db, user)

    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )


# Get user
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = crud.get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

# Login API
@app.post("/auth/login", response_model=schemas.TokenResponse)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    # Step 1: Find user in database
    db_user = crud.get_user_by_username(db, user.username)

    # Step 2: Check whether user exists
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Step 3: Verify password
    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Step 4: Check account status
    if not db_user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account is inactive"
        )

    # Step 5: Generate JWT
    access_token = create_access_token(
        user_id=db_user.id,
        username=db_user.username
    )

    # Step 6: Return token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/users/me", response_model=schemas.UserResponse)
def get_me(
    current_user = Depends(get_current_user)
):
    return current_user