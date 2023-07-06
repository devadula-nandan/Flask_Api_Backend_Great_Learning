<!-- '{"name":"Flask Api","version": 12,"tech": ["Rest Api", "Flask", "MySql", "ORM"],"tags":["api","backend"],"snapshots":[]}' -->
# Python Version: 3.9.9
# Virtual Environment Created in Windows 11

**Note:** If you are using SQLite, please be aware that SQLite has limitations in certain aspects. For example, SQLite doesn't convert UUID4 to a string automatically like MySQL does. Therefore, MySQL is preferred. If you want to use SQLite, make sure to typecast the UUIDs to string.

## Quiz Creation

- When creating a quiz, if you enter the same question ID more than once, it will only be added once.

## Unwanted Imports and Datetime

- There may be some unwanted imports initially included. Feel free to remove them as needed.
- We don't explicitly insert the `updated_ts` (updated timestamp) every time. Instead, we use SQLAlchemy's built-in `onupdate` feature at the database level.

## Attempting a Quiz

When making a request to attempt a quiz, the response should be in the following format:

```json
{
  "quiz_id": "string",
  "responses": {
    "question_id": "response",
    "question_id": "response",
    "question_id": "response"
  },
  "session_id": "string"
}
```

# Example

```json
{
  "quiz_id": "21013492",
  "responses": {
    "82987650": 2,
    "31420463": 4,
    "29391564": 3
  },
  "session_id": "76f3f47d-7c72-4355-b5f2-a64147a6a2db"
}
```

# Swagger URL

You can use the following URL to access the Swagger UI for API testing and documentation:

[http://127.0.0.1:8000/swagger-ui/](http://127.0.0.1:8000/swagger-ui/)

# Improvements

Consider the following improvements for your application:

- Implement a "Sign Out of All Devices" feature to enhance security.
- Use cookies to get and set the session ID in the response body for a persistent user experience.
- The current implementation uses the first 8 digits of the UUID4 integer for ID generation in tables. You may want to consider alternatives such as auto-incrementing primary keys or modifying the UUID generation process. The UUID generation logic is wrapped in a function and can be modified wherever required.
