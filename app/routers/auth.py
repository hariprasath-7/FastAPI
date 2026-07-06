from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.routers import user
from ..import database, schemas, model, utils, oauth

router = APIRouter(tags=["Authentication"])

# @router.post("/login")
# def login(
#     user_credentials: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(database.get_db)
# ):

@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    print("Username:", user_credentials.username)

    user = db.query(model.User).filter(
        model.User.email == user_credentials.username
    ).first()

    print("User:", user)

    if not user:
        raise HTTPException(status_code=404, detail="Invalid credentials")

    print("Password entered:", user_credentials.password)
    print("Password in DB:", user.password)

    result = utils.verify(user_credentials.password, user.password)
    print("Password match:", result)

    if not result:
        raise HTTPException(status_code=404, detail="Invalid credentials")

    access_token = oauth.create_access_token(data={"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

    # user = db.query(model.User).filter(model.User.email == user_credentials.username).first()

    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    # if not utils.verify(user_credentials.password, user.password):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    # access_token = oauth.create_access_token(data={"user_id": user.id})

    # return {"access_token": access_token, "token_type": "bearer"}
