from sqlalchemy.orm import Session
from ..database.database import get_db
from ..crud.crud import get_user_by_email, create_user
from ..schemas.schemas import UserCreate, User
from fastapi import (APIRouter, Depends,
                     HTTPException, status)

router = APIRouter()


@router.post("/users/", tags=["users"], response_model=User)
async def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered")
    elif not db_user:
        create_user(db=db, user=user)
        raise HTTPException(status_code=status.HTTP_201_CREATED,
                            detail="User was created!",
                            headers={"WWW-Authenticate": "Bearer"})


# @router.get("/users/me", tags=["users"])
# async def read_user_me():
#     return {"username": "fakecurrentuser"}


# @router.get("/users/{username}", tags=["users"])
# async def read_user(username: str):
#     return {"username": username}
