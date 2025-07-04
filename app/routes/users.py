from app.models.user import User,UserPublic,UserCreate,AppOwner

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.db import get_session
from app.auth import create_access_token,get_password_hash,verify_password
from app.auth import get_current_user

router = APIRouter()

def login_asowner_Depends(db: Session = Depends(get_session), current_user: dict = Depends(get_current_user)):
    owner = db.query(AppOwner).filter(AppOwner.username == current_user["username"]).first()
    if not owner:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perform this action")
    return current_user

@router.post("/register", response_model=UserPublic)
def register_user(user: UserCreate, db: Session = Depends(get_session)):

    db_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password)
        )
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    existing_owner = db.query(AppOwner).filter(AppOwner.username == user.username).first()
    if existing_owner:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Owner already exists")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_name}", response_model=UserPublic)
def get_user(user_name: str, db: Session = Depends(get_session)):
    db_user = db.query(User).filter(User.username == user_name).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.delete("/delete/{user_name}")
def delete_user(user_name: str, db: Session = Depends(get_session),owner: dict = Depends(login_asowner_Depends)):
    db_user = db.query(User).filter(User.username == user_name).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = db.query(User).filter(User.username == form_data.username).first()	
    owner = db.query(AppOwner).filter(AppOwner.username == form_data.username).first()
    if not user:
        if not owner:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if not verify_password(form_data.password, owner.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        access_token = create_access_token(data={"sub": owner.username})
        return {"access_token": access_token, "token_type": "bearer"}
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
