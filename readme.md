# python version 3.9.9
# virtual environment created in win 11
# note if you are using sqlite, sqlite has limitations in certain aspects like sqlite does'nt convert uuid4 to a string while mysql does, so mysql is prefered, if u wanna use sqlite, please typecast the uuids to string


# while creating quiz, if we enter a same question id more than 1 time, only once it will be added

# there will be some unwanted imports which were initially given, they can be removed, as we don't insert datetime for updated_ts everytime, instead we use sql alchemy's built in onupdate db level feature

# in attempt quiz api, the responese should be in the following format
{
  "quiz_id": "string",
  "responses": {
    "question_id": response,
    "question_id": response,
    "question_id": response
  },
  "session_id": "string"
}

# example
{
  "quiz_id": "21013492",
  "responses": {
    "82987650": 2,
    "31420463": 4,
    "29391564": 3
  },
  "session_id": "76f3f47d-7c72-4355-b5f2-a64147a6a2db"
}

# swagger url for api testing and docs
http://127.0.0.1:8000/swagger-ui/

# improvements
sign out of all devices can be implemented
get and set cookies can be used with the response body, for session id for a persistant user experience.
the 8 digits of uuid4 int is used for id generation in tables, which can be replaced, with auto incrementing primary keys, or the uuid generation can be tweaked, as it is wrapped in a function, and is called wherever required