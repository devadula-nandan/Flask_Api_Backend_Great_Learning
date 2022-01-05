from sqlalchemy.orm.session import sessionmaker
from app.models import QuestionMaster, QuizInstance, QuizMaster, QuizQuestions, UserMaster, UserResponses, UserSession
from app import db
import uuid
from flask import session
import datetime
from typing import List

"""
[Services Module] Implement various helper functions here as a part of api
                    implementation using MVC Template
"""

# utility functions

def saveData(data=None) : 
    if data : 
        db.session.add(data)
    db.session.commit()

def generateId() : 
    return str(uuid.uuid4().int)[:8]  

def getUser(**kwargs) : 
    return UserMaster.query.filter_by(**kwargs).first()

def getUserSession(session_id) : 
    return UserSession.query.filter_by(session_id=session_id, is_active=True).first()

def getAdminSession(session_id) : 
    session = getUserSession(session_id)
    if not session : 
        return
    admin = UserMaster.query.filter_by(id=session.user_id, is_admin=True).count()
    if admin : 
        return session

def getQuestionList(questions) : 
    questionList = []
    for question in questions : 
        _question = {
            'id': question.id,
            'question': question.question,
            'choice1': question.choice1,
            'choice2': question.choice2,
            'choice3': question.choice3,
            'choice4': question.choice4,
            'answer': question.answer,
            'marks': question.marks,
            'remarks': question.remarks,
        }
        questionList.append(_question)
    return questionList

def getQuizList(quizzes) : 
    quizList = []
    for quiz in quizzes : 
        _quiz = {
            'id': quiz.id,
            'quiz_name': quiz.quiz_name
        }
        quizList.append(_quiz)
    return quizList

def getAssignedQuizList(quizzes) : 
    quizList = []
    for quiz in quizzes : 
        print(quiz)
        quiz_master = QuizMaster.query.filter_by(id=quiz.quiz_id).first()
        _quiz = {
            'id': quiz.id,
            'user_id': quiz.user_id,
            'quiz_id': quiz.quiz_id,
            'quiz_name': quiz_master.quiz_name,
            'score_achieved': quiz.score_achieved,
            'is_submitted': quiz.is_submitted,
        }
        quizList.append(_quiz)
    return quizList

# api controllers

def signUp(**kwargs) : 
    if not len(kwargs.values()) or None in kwargs.values() : 
        return {'message': 'Incomplete information provided', 'status_code': 400}
    user = getUser(username=kwargs['username'])
    if user : 
        return {'message': 'Username already exists.', "status_code": 400}
    user = UserMaster(
            id=generateId(),
            **kwargs
        )
    saveData(user)
    return {
        'message': f'new {"admin" if kwargs["is_admin"] else "user"} account created.',
        'status_code': 201,
    }

def login(**kwargs) : 
    if not len(kwargs.values()) or None in kwargs.values() : 
        return {'message': 'Incomplete information provided', 'status_code': 400}
    user = getUser(**kwargs)
    if not user : 
        return {
            'message': 'Invalid information provided',
            'status_code': 401
        }   
    session_id = uuid.uuid4()
    user_session = UserSession(
            id=generateId(),
            user_id=user.id,
            session_id=session_id,
        )
    saveData(user_session)
    return {
        'message': 'Logged in successfully',
        'session_id': session_id,
        'status_code': 200,
    }

def logout(**kwargs) : 
    session_id = kwargs.get('session_id')
    if not session_id : 
        return {'message': 'No session ID', 'status_code': 400}
    session = getUserSession(session_id)
    if session : 
        UserSession.query.filter_by(session_id=session_id, is_active=True).delete()
        saveData()
        return {'message': 'Logged out successfully', 'status_code': 200}
    else : 
        return {'message': 'Session does not exist.', 'status_code': 403}

def addQuestion(**kwargs) : 
    if not len(kwargs.values()) or None in kwargs.values() : 
        return {'message': 'Incomplete information provided', 'status_code': 400}
    session = getAdminSession(kwargs.pop("session_id"))
    if not session : 
        return {'message': 'Unauthorized', 'status_code': 401}
    question = QuestionMaster(
            id=generateId(),
            **kwargs
        )
    saveData(question)
    return {'message': 'New question added.', 'status_code': 201}

def listAllQuestions(**kwargs) : 
    session_id = kwargs.get('session_id')
    if not session_id : 
        return {'message': 'No session ID', 'status_code': 400}
    session = getAdminSession(session_id)
    if not session : 
        return {'message': 'Unauthorized', 'status_code': 401}
    questions = QuestionMaster.query.all()
    questionList = getQuestionList(questions)
    return {'message': f'{len(questions)} (all) question(s) fetched.', 'questions': questionList, 'status_code': 200}

def createQuiz(**kwargs) : 
    if not len(kwargs.values()) or None in list(kwargs.values()) : 
        return {'message': 'Incomplete information provided', 'status_code': 400}
    if not getAdminSession(kwargs['session_id']) : 
        return {'message': 'Unauthorized', 'status_code': 401}
    quiz = QuizMaster(
            id=generateId(),
            quiz_name=kwargs['quiz_name']
        )
    saveData(quiz)
    for question_id in set(kwargs['questions']) : 
        if not QuestionMaster.query.filter_by(id=question_id).count() : 
            return {'message': 'Invalid questions provided.', 'status_code': 400}
        quiz_question = QuizQuestions(
                id=generateId(),
                quiz_id=quiz.id,
                question_id=question_id,
            )
        saveData(quiz_question)
    return {'message': 'New quiz created.', 'status_code': 201}

def assignQuiz(**kwargs) : 
    if not len(kwargs.values()) or None in kwargs.values() : 
        return {'message': 'Incomplete information provided', 'status_code': 400}
    if not getAdminSession(kwargs.pop('session_id')) : 
        return {'message': 'Unauthorized', 'status_code': 401}
    if not QuizMaster.query.filter_by(id=kwargs['quiz_id']).count() : 
        return {'message': 'Quiz does not exist.', 'status_code': 400}
    if not UserMaster.query.filter_by(id=kwargs['user_id']).count() : 
        return {'message': 'User does not exist.', 'status_code': 400}
    if QuizInstance.query.filter_by(user_id=kwargs['user_id'], quiz_id=kwargs['quiz_id'], is_submitted=False).count() : 
        return {'message': 'Quiz already assigned.', 'status_code': 403}
    assigned_quiz = QuizInstance(
            id=generateId(),
            **kwargs
        )
    saveData(assigned_quiz)
    return {'message': 'Quiz assigned.', 'status_code': 201}

def viewQuiz(**kwargs) : 
    if None in list(kwargs.values()) :  
        return {'message': 'Incomplete information provided.', 'status_code': 400}
    quiz_id, session_id = kwargs['quiz_id'], kwargs.get('session_id')
    if not session_id : 
        return {'message': 'Not logged in.', 'status_code': 400}
    quiz = QuizMaster.query.filter_by(id=quiz_id).first()
    if not quiz : 
        return {'message': 'Quiz does not exist.', 'status_code': 400}
    session = getUserSession(session_id)
    if not session : 
        return {'message': 'Not logged in.', 'status_code': 403}
    if getAdminSession(session_id) or QuizInstance.query.filter_by(quiz_id=quiz_id, user_id=session.user_id).count() : 
        quiz_questions = QuizQuestions.query.filter_by(quiz_id=quiz_id)
        questions = []
        for quiz_question in quiz_questions : 
            questions.append(QuestionMaster.query.filter_by(id=quiz_question.question_id).first())
        questionList = getQuestionList(questions)
        return {'message': f'Quiz has {len(questionList)} question(s)', 'questions': questionList, 'status_code': 200}
    else : 
        return {'message': 'Unauthorized', 'status_code': 401}

def viewAssignedQuizzes(**kwargs) : 
    session_id = kwargs.get('session_id')
    if not session_id : 
        return {'message': 'No session ID.', 'status_code': 400}
    session = getUserSession(session_id)
    if not session : 
        return {'message': 'Not logged in.', 'status_code': 403}
    quizzes = QuizInstance.query.filter_by(user_id=session.user_id).all()
    quizList = getAssignedQuizList(quizzes)
    return {'message': f'{len(quizzes)} quiz(zes) assigned', 'quizzes': quizList, 'status_code': 200} 

def viewAllQuizzes(**kwargs) : 
    session_id = kwargs.get('session_id')
    if not session_id : 
        return {'message': 'No session ID.', 'status_code': 400}
    if not getAdminSession(session_id) : 
        return {'message': 'Unauthorized', 'status_code': 401}
    quizzes = QuizMaster.query.all()
    quizList = getQuizList(quizzes)
    return {'message': f'{len(quizzes)} quiz(zes) fetched.', 'quizzes': quizList, 'status_code': 200}

def attemptQuiz(**kwargs) : 
    if not len(kwargs.values()) or None in kwargs.values() :  
        return {'message': 'Incomplete information provided.', 'status_code': 400}
    session = getUserSession(kwargs.pop('session_id'))
    if not session : 
        return {'message': 'Not logged in.', 'status_code': 403}
    quiz_id, responses = kwargs['quiz_id'], kwargs['responses']
    if not QuizMaster.query.filter_by(id=quiz_id).count() : 
        return {'message': 'Quiz does not exist.', 'status_code': 400}
    quiz_instance = QuizInstance.query.filter_by(quiz_id=quiz_id, user_id=session.user_id).first()
    if not quiz_instance : 
        return {'message': 'Quiz not assigned.', 'status_code': 401}
    if quiz_instance.is_submitted : 
        return {'message': 'Quiz already submitted.', 'status_code': 403}
    quiz_questions = QuizQuestions.query.filter_by(quiz_id=quiz_id).all()
    if len(quiz_questions) != len(responses) : 
        return {'message': 'Incomplete/Invalid responses.', 'status_code': 400}
    questions = {}
    for quiz_question in quiz_questions : 
        questions[quiz_question.question_id] = QuestionMaster.query.filter_by(id=quiz_question.question_id).first()
    score = 0
    for question_id in questions : 
        try : 
            if questions[question_id].answer == responses[question_id] : 
                score += questions[question_id].marks
        except : 
            return {'message': 'Invalid response.', 'status_code': 400}
    for question_id in questions : 
        user_response = UserResponses(
                id=generateId(),
                quiz_id=quiz_id,
                user_id=session.user_id,
                question_id=question_id,
                response=responses[question_id],
            )
        saveData(user_response)
    quiz_instance.score_achieved = score
    quiz_instance.is_submitted = True
    saveData()
    return {'message': f'Quiz attempted, Score : {score}.', 'status_code': 200}

def quizResults(**kwargs) : 
    session_id = kwargs.get('session_id')
    if not session_id : 
        return {'message': 'No session ID.', 'status_code': 400}
    if not getAdminSession(session_id) : 
        return {'message': 'Unauthorized', 'status_code': 401}
    results = QuizInstance.query.filter_by(quiz_id = kwargs["quiz_id"]).order_by(QuizInstance.score_achieved.desc(),QuizInstance.is_submitted.desc()).all()
    resultList = getAssignedQuizList(results)
    return {'message': f'{len(results)} result(s) fetched.', 'results': resultList, 'status_code': 200}