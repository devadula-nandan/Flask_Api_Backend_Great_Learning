from marshmallow import Schema, fields

# request schemas

class SignUpRequest(Schema):
    name = fields.Str()
    username = fields.Str()
    password = fields.Str()
    is_admin = fields.Boolean(missing=False,allow_none=True)

class LoginRequest(Schema):
    username = fields.Str()
    password = fields.Str()

class SessionRequest(Schema):
    session_id = fields.Str()

class AddQuestionRequest(Schema) : 
	question = fields.Str() 
	choice1 = fields.Str()
	choice2 = fields.Str()
	choice3 = fields.Str()
	choice4 = fields.Str()
	answer = fields.Int()
	marks = fields.Int()
	remarks = fields.Str()
	session_id = fields.Str()

class CreateQuizRequest(Schema) : 
	quiz_name = fields.Str()
	questions = fields.List(fields.Str())
	session_id = fields.Str()

class AssignQuizRequest(Schema) : 
	quiz_id = fields.Str()
	user_id = fields.Str()
	session_id = fields.Str()

class QuizResultRequest(Schema) : 
	quiz_id = fields.Str()
	session_id = fields.Str()

class ViewQuizRequest(Schema) : 
	quiz_id = fields.Str()
	session_id = fields.Str()

class AttemptQuizRequest(Schema) : 
	quiz_id = fields.Str()
	responses = fields.Dict(keys=fields.Str(), values=fields.Int())
	session_id = fields.Str()

# response schemas

class BaseResponse(Schema) : 
	message = fields.Str()

class LoginResponse(Schema) : 
	message = fields.Str()
	session_id = fields.Str()

class ListResponse(Schema) : 
	message = fields.Str()
	results = fields.List(fields.Dict())