from sqlalchemy.orm import Session
import datetime
from ..models.users import Users
import uuid


class Crud:
    # def get_user(db: Session, user_id: int):
    #     return db.query(Users).filter(Users.User.id == user_id).first()

    def get_user_by_email(db: Session, email: str):
        return db.query(Users).filter(Users.email == email).first()

    def get_user_by_public_id(db: Session, public_id: str):
        return db.query(Users).filter(Users.public_id == public_id).first()

    def get_user_by_username(db: Session, username: str):
        return db.query(Users).filter(Users.username == username).first()

    # def get_user_by_username_auth(db: Session, username: str):
    #     return db.query(User).filter(User.username == username).first()

    # def get_users(db: Session, skip: int = 0, limit: int = 100):
    #     return db.query(User).offset(skip).limit(limit).all()

    def update_user(current_user, db: Session, payload: dict):
        current_user.firstname = payload.firstname
        current_user.lastname = payload.lastname
        db.commit()
        db.refresh(current_user)
        return current_user

    def confirm_account(db: Session, public_id: str):
        user = db.query(Users).filter(Users.public_id == public_id).first()
        user.confirmed = True
        db.commit()
        db.refresh(user)
        return user

    def create_user(db: Session, UserCreateSchema, hashed_password):
        public_id = str(uuid.uuid4())
        newUser = Users(username=UserCreateSchema.username,
                        firstname=UserCreateSchema.firstname,
                        lastname=UserCreateSchema.lastname,
                        email=UserCreateSchema.email, password=hashed_password,
                        public_id=public_id,
                        register_date=datetime.datetime.now())
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        return newUser
