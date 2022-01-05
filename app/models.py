import enum
from sqlalchemy.sql import func
from app import application
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum

"""
[DataBase Access Details]
Below is the configuration mentioned by which the application can make connection with MySQL database
"""
username = 'root'
password = 'nandan123'
database_name = 'quiz_app'
application.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{username}:{password}@localhost/{database_name}"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(application)

class UserMaster(db.Model):
    __tablename__ = 'user_master'

    id = Column(String(100), primary_key=True)
    name = Column(String(200))
    username = Column(String(200), unique=True)
    password = Column(String(200))
    is_admin = Column(Boolean)
    is_active = Column(Boolean, default=True)
    created_ts = Column(DateTime, default=func.now())
    updated_ts = Column(DateTime, onupdate=func.now())

    def __init__(self, id, name, username, password, is_admin):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.is_admin = is_admin
            
class UserSession(db.Model):
        __tablename__ = 'user_session'

        id = Column(String(100), primary_key=True)
        user_id = Column(String(100), ForeignKey("user_master.id"))
        session_id = Column(String(200), unique=True)
        is_active = Column(Boolean, default=True)
        created_ts = Column(DateTime, default=func.now())
        updated_ts = Column(DateTime, onupdate=func.now())
        
        def __init__(self, id, user_id, session_id):
            self.id = id
            self.user_id = user_id
            self.session_id = session_id
        
class QuestionMaster(db.Model):
        __tablename__ = 'question_master'

        id = Column(String(100), primary_key=True)
        question = Column(String(500), index=True)
        choice1 = Column(String(500))
        choice2 = Column(String(500))
        choice3 = Column(String(500))
        choice4 = Column(String(500))
        answer = Column(Integer)
        marks = Column(Integer)
        remarks = Column(String(200))
        is_active = Column(Boolean, default=True)
        created_ts = Column(DateTime, server_default=func.now())
        updated_ts = Column(DateTime, onupdate=func.now())
        
        def __init__(self, id, question, choice1, choice2, choice3, choice4, answer, marks, remarks):
            self.id = id
            self.question = question
            self.choice1 = choice1
            self.choice2 = choice2
            self.choice3 = choice3
            self.choice4 = choice4
            self.answer = answer
            self.marks = marks
            self.remarks = remarks
            
class QuizMaster(db.Model):
        __tablename__ = 'quiz_master'

        id = Column(String(100), primary_key=True)
        quiz_name = Column(String(200))
        is_active = Column(Boolean, default=True)
        created_ts = Column(DateTime, server_default=func.now())
        updated_ts = Column(DateTime, onupdate=func.now())
        
        def __init__(self, id, quiz_name):
            self.id = id
            self.quiz_name = quiz_name
            
class QuizQuestions(db.Model):
        __tablename__ = 'quiz_questions'

        id = Column(String(100), primary_key=True)
        quiz_id = Column(String(100), ForeignKey("quiz_master.id"))
        question_id = Column(String(100), ForeignKey("question_master.id"))
        is_active = Column(Boolean, default=True)
        created_ts = Column(DateTime, server_default=func.now())
        updated_ts = Column(DateTime, onupdate=func.now())
        
        def __init__(self, id, quiz_id, question_id):
            self.id = id
            self.quiz_id = quiz_id
            self.question_id = question_id
     
class QuizInstance(db.Model):
        __tablename__ = 'quiz_instance'

        id = Column(String(100), primary_key=True)
        quiz_id = Column(String(100), ForeignKey("quiz_master.id"))
        user_id = Column(String(100), ForeignKey("user_master.id"))
        score_achieved = Column(Integer, default=0)
        is_submitted = Column(Boolean, default=False)
        is_active = Column(Boolean, default=True)
        created_ts = Column(DateTime, server_default=func.now())
        updated_ts = Column(DateTime, onupdate=func.now())
        
        def __init__(self, id, quiz_id, user_id):
            self.id = id
            self.quiz_id = quiz_id
            self.user_id = user_id
            
class UserResponses(db.Model):
        __tablename__ = 'user_responses'

        id = Column(String(100), primary_key=True)
        quiz_id = Column(String(100), ForeignKey("quiz_master.id"))
        user_id = Column(String(100), ForeignKey("user_master.id"))
        question_id = Column(String(100), ForeignKey("question_master.id"))
        response = Column(Integer)
        is_active = Column(Boolean, default=True)
        created_ts = Column(DateTime, server_default=func.now())
        updated_ts = Column(DateTime, onupdate=func.now())        

        def __init__(self, id, quiz_id, user_id, question_id, response):
            self.id = id
            self.quiz_id = quiz_id
            self.user_id = user_id
            self.question_id = question_id
            self.response = response
    
db.create_all()
db.session.commit()