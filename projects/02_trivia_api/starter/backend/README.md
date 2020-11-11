# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.

Endpoints
GET '/categories'
GET '/questions'
GET '/categories/<int:category_id>/questions'
POST '/questions'
POST '/quizzes'
DELETE '/questions/<int:id>'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
    {'1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"}
- Response Code: 200 if categories returned successfully

GET '/questions'
- Fetches a dictionary of paginated questions, so this end point uses argument 'page'
- Request Arguments: 'page'
- Returns: A json object that contains questions, total_questions, categories and current_Category
    as question: is the paginated questions returned,
    total_questions: is number of all exisiting questions,
    categories: all exisiting categories,
    current_Category: current category if specified
- Response Code: 200 if questions returned successfully
                or 404 if page number contains no questions

GET '/categories/<int:category_id>/questions'
- Fetches a dictionary of questions related to specific category
- URL Parameters: category_id
- Returns: A json object that contains questions, total_questions, categories and current_Category as:
    question: is the questions related to category chosen,
    total_questions: is number of all returned questions,
    categories: all exisiting categories,
    current_Category: current category specified
- Response Code: 200 if questions returned successfully
                or 404 if there is no questions or categories

POST '/questions'
- this endpoint is used for 2 reasons:
    1-used to add question
    2-used to search for questions with specific characters
- Request Arguments:
    1- Adding question: question, answer, difficulty, category as:
        question: which is a string of a question to be added
        answer: which is a string of an answer of this question
        difficulty: it's a number describing the difficulty of the question
        category: id of a category that question is related to
    2- Search for a question: searchTerm
        searchTerm: used to find all questions that contain this string
- Returns:
    1- Adding question: success, created
        success: is a flag returns true if adding is done successfully
        created: contains id of the question created
    2- Search for a question: questions, total_questions, current_Category
        question: questions containing the string searchTerm,
        current_Category: current category if specified
- Response Code:
        1- Adding question:200 if questions created successfully
                or 400 if one of the arguments not filled
        2- Search for a question:200 if search is successful

POST '/quizzes'
- this endpoint is used for the play, it's used to accept category as an argument to limit type of questions to Play or choose from all categories too,
    also accept previous questions so that a question only appear once
- Request Arguments: previous_questions, quiz_category
    previous_questions: id of answered question
    quiz_category: object (dictionary) contains id and type of selected category
- Returns: question, answer
    question: contains one question or False
    answer: contains answer of the question if exist or False
- Response Code: 200 

DELETE '/questions/<int:id>'
- this endpoint is used to delete a specific question
- URL Parameters: id of the question to be deleted
- Returns:
    success: is a flag returns true if deleting is done successfully
    deleted: contains id of the question deleted
- Response Code: 200 if questions deleted successfully
                or 422 if id of the question not exist

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
