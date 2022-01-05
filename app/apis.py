from app.models import *
from app import *
from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from app.schemas import *
from app.services import *
from flask import request

"""
[Sign Up API] : Its responsibility is to perform the signup activity for the user.
"""
#  Restful way of creating APIs through Flask Restful
class SignUpAPI(MethodResource, Resource):
    @doc(description='Sign up for a new user account.', tags=['User'])
    @use_kwargs(SignUpRequest, location=('json'))
    @marshal_with(BaseResponse)
    def post(self, **kwargs) : 
        response = signUp(**kwargs)
        return BaseResponse().dump({'message': response['message']}), response['status_code']

api.add_resource(SignUpAPI, '/signup')
docs.register(SignUpAPI)

"""
[Login API] : Its responsibility is to perform the login activity for the user and 
create session id which will be used for all subsequent operations.
"""
class LoginAPI(MethodResource, Resource):
    @doc(description='Login to get back a session ID.', tags=['User'])
    @use_kwargs(LoginRequest, location=('json'))
    @marshal_with(LoginResponse)
    def post(self, **kwargs) : 
        response = login(**kwargs)
        return LoginResponse().dump({
                'message': response['message'], 
                'session_id': response.get('session_id')
            }), response['status_code']
            
api.add_resource(LoginAPI, '/login')
docs.register(LoginAPI)

"""
[Logout API] : Its responsibility is to perform the logout activity for the user.
"""
class LogoutAPI(MethodResource, Resource):
    @doc(description='Logout of the session.', tags=['User'])
    @use_kwargs(SessionRequest, location=('json'))
    @marshal_with(BaseResponse)
    def delete(self, **kwargs) : 
        response = logout(**kwargs)
        return BaseResponse().dump({
                'message': response['message'],
            }), response['status_code']
            
api.add_resource(LogoutAPI, '/logout')
docs.register(LogoutAPI)

"""
[Add Question API] : Its responsibility is to add question to the question bank.
Admin has only the rights to perform this activity.
"""
class AddQuestionAPI(MethodResource, Resource):
    @doc(description='Admin can add a new question.', tags=['Question (admin)'])
    @use_kwargs(AddQuestionRequest, location=('json'))
    @marshal_with(BaseResponse)
    def post(self, **kwargs) : 
        response = addQuestion(**kwargs)
        return BaseResponse().dump({
                'message': response['message'],
            }), response['status_code']

api.add_resource(AddQuestionAPI, '/add.question')
docs.register(AddQuestionAPI)

"""
[List Questions API] : Its responsibility is to list all questions present activly in the question bank.
Here only Admin can access all the questions.
"""
class ListQuestionAPI(MethodResource, Resource):
    @doc(description='Admin can list all the questions.', tags=['Question (admin)'])
    @use_kwargs(SessionRequest, location=('json'))
    @marshal_with(ListResponse)
    def post(self, **kwargs) : 
        response = listAllQuestions(**kwargs)
        return ListResponse().dump({
                'message': response['message'],
                'results': response.get('questions')
            }), response['status_code']

api.add_resource(ListQuestionAPI, '/list.questions')
docs.register(ListQuestionAPI)

"""
[Create Quiz API] : Its responsibility is to create quiz and only admin can create quiz using this API.
"""
class CreateQuizAPI(MethodResource, Resource):
    @doc(description='Admin can create a new quiz.', tags=['Quiz (admin)'])
    @use_kwargs(CreateQuizRequest, location=('json'))
    @marshal_with(BaseResponse)
    def post(self, **kwargs) : 
        response = createQuiz(**kwargs)
        return BaseResponse().dump({
                'message': response['message'],
            }), response['status_code']

api.add_resource(CreateQuizAPI, '/create.quiz')
docs.register(CreateQuizAPI)

"""
[Assign Quiz API] : Its responsibility is to assign quiz to the user. Only Admin can perform this API call.
"""
class AssignQuizAPI(MethodResource, Resource):
    @doc(description='Admin can assign a quiz to an user.', tags=['Quiz (admin)'])
    @use_kwargs(AssignQuizRequest, location=('json'))
    @marshal_with(BaseResponse)
    def post(self, **kwargs) : 
        response = assignQuiz(**kwargs)
        return BaseResponse().dump({
                'message': response['message'],
            }), response['status_code']

api.add_resource(AssignQuizAPI, '/assign.quiz')
docs.register(AssignQuizAPI)

"""
[View Quiz API] : Its responsibility is to view the quiz details.
Only Admin and the assigned users to this quiz can access the quiz details.
"""
class ViewQuizAPI(MethodResource, Resource):
    @doc(description='Questions of created or assigned quiz can be viewed.', tags=['Quiz (admin) (user)'])
    @use_kwargs(ViewQuizRequest, location=('json'))
    @marshal_with(ListResponse)
    def post(self, **kwargs) :
        response = viewQuiz(**kwargs)
        return ListResponse().dump({
                'message': response['message'],
                'results': response.get('questions')
            }), response['status_code']

api.add_resource(ViewQuizAPI, '/view.quiz')
docs.register(ViewQuizAPI)

"""
[View Assigned Quiz API] : Its responsibility is to list all the assigned quizzes 
                            with there submittion status and achieved scores.
"""
class ViewAssignedQuizAPI(MethodResource, Resource):
    @doc(description='View all the assigned quizzes.', tags=['Quiz (user)'])
    @use_kwargs(SessionRequest, location=('json'))
    @marshal_with(ListResponse)
    def post(self, **kwargs) : 
        response = viewAssignedQuizzes(**kwargs)
        return ListResponse().dump({
                'message': response['message'],
                'results': response.get('quizzes')
            }), response['status_code']

api.add_resource(ViewAssignedQuizAPI, '/assigned.quizzes')
docs.register(ViewAssignedQuizAPI)

"""
[View All Quiz API] : Its responsibility is to list all the created quizzes. Admin can only list all quizzes.
"""
class ViewAllQuizAPI(MethodResource, Resource):
    @doc(description='Admin can View all the created quizzes.', tags=['Quiz (admin)'])
    @use_kwargs(SessionRequest, location=('json'))
    @marshal_with(ListResponse)
    def post(self, **kwargs) : 
        response = viewAllQuizzes(**kwargs)
        return ListResponse().dump({
                'message': response['message'],
                'results': response.get('quizzes')
            }), response['status_code']

api.add_resource(ViewAllQuizAPI, '/all.quizzes')
docs.register(ViewAllQuizAPI)

"""
[Attempt Quiz API] : Its responsibility is to perform quiz attempt activity by 
                        the user and the score will be shown as a result of the submitted attempt.
"""
class AttemptQuizAPI(MethodResource, Resource):
    @doc(description='Attempt a quiz by submitting responses.', tags=['Quiz (user)'])
    @use_kwargs(AttemptQuizRequest, location=('json'))
    @marshal_with(BaseResponse)
    def post(self, **kwargs) : 
        response = attemptQuiz(**kwargs)
        return BaseResponse().dump({
                'message': response['message']
            }), response['status_code']

api.add_resource(AttemptQuizAPI, '/attempt.quiz')
docs.register(AttemptQuizAPI)

"""
[Quiz Results API] : Its responsibility is to provide the quiz results in which the users 
                        having the scores sorted in descending order are displayed, 
                        also the ones who have not attempted are also shown.
                        Admin has only acess to this functionality.
"""
class QuizResultAPI(MethodResource, Resource):
    @doc(description='Admin can View quiz results.', tags=['Quiz (admin)'])
    @use_kwargs(QuizResultRequest, location=('json'))
    @marshal_with(ListResponse)
    def post(self, **kwargs) : 
        response = quizResults(**kwargs)
        return ListResponse().dump({
                'message': response['message'],
                'results': response.get('results')
            }), response['status_code']

api.add_resource(QuizResultAPI, '/quiz.results')
docs.register(QuizResultAPI)