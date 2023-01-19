from sqlalchemy.orm import Session
import datetime
from ..models import users as User
import uuid


class Crud:
    def get_user(db: Session, user_id: int):
        return db.query(User).filter(User.User.id == user_id).first()

    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_user_by_public_id(db: Session, public_id: str):
        return db.query(User).filter(User.public_id == public_id).first()

    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def get_user_by_username_auth(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def get_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    def confirm_account(db: Session, public_id: str):
        user = db.query(User).filter(User.public_id == public_id).first()
        user.confirmed = True
        db.commit()
        db.refresh(user)
        return user

    def create_user(db: Session, UserCreateSchema, hashed_password):
        public_id = str(uuid.uuid4())
        newUser = User(username=UserCreateSchema.username,
                       firstname=UserCreateSchema.firstname,
                       lastname=UserCreateSchema.lastname,
                       email=UserCreateSchema.email, password=hashed_password,
                       public_id=public_id,
                       register_date=datetime.datetime.now())
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        return newUser
