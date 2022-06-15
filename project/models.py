from enum import unique
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from project import db


class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False, unique=False)
    
    task_lists = relationship("TaskList", back_populates="user")


    def __repr__(self) -> str:
        return f"<user : {self.username}>"


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.String(200), unique=False, nullable=False)
    status = db.Column(db.String(20), unique=False, nullable=False)
    
    task_list_id = db.Column(db.Integer, db.ForeignKey("task_list.id"))

    
    task_list = relationship("TaskList", back_populates="tasks")

    def __repr__(self) -> str:
        return f"<user : {self.id}>"

class TaskList(db.Model):
    __tablename__ = "task_list"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), unique=True, nullable=False)
    date = db.Column(db.Date(), unique=False, nullable=False)
    user_id = user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    tasks = relationship("Task", back_populates="task_list")
    user = relationship("Users", back_populates="task_lists")
    

    def __repr__(self) -> str:
        return f"<user : {self.id}>"


# <script src="https://kit.fontawesome.com/5d8f290e4a.js" crossorigin="anonymous"></script>
