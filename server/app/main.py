from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import engine, Base
from dotenv import load_dotenv
from models.userModels import User
from aws import AWS_Cognito, get_aws_cognito, SignUpModel

load_dotenv()
app = FastAPI()


Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"hello": "world"}

@app.get("/users")
def fetch_users_data():
    with Session(engine) as session:
        try:
            result = session.query(User).all()
            return result
        except SQLAlchemyError as exc:
                print(exc)
                return {"error_message": "Get execution error"}



@app.post("/user")
def create_user_data(username : str, age:int):
    with Session(engine) as session:
        try:
            res = User(username=username, age=age)
            session.add(res)
            session.commit()
            session.refresh(res)
            return res
        except SQLAlchemyError as exc:
                session.rollback()
                print(exc)
                return {"error_message": "Insert execution error"}
        
@app.put("/user")
def update_user_data(user_id:int, username:str):
    with Session(engine) as session:
        try:
            res = session.query(User).filter(User.id == user_id).first()
            if res:
                 setattr(res, "username", username)
                 session.commit()
                 session.refresh(res)
            return res
        except SQLAlchemyError as exc:
                session.rollback()
                print(exc)
                return {"error_message": "Update execution error"}


@app.delete("/user")
def delete_user(user_id:int):
    with Session(engine) as session:
        try:
            res = session.query(User).filter(User.id == user_id).first()
            if res:
                 session.delete(res)
                 session.commit()
            return res
        except SQLAlchemyError as exc:
                session.rollback()
                print(exc)
                return {"error_message": "Delete execution error"}
        
@app.post("/sign_up")
def sign_up(user: SignUpModel, cognito: AWS_Cognito = Depends(get_aws_cognito)):
     return cognito.sign_up(user)