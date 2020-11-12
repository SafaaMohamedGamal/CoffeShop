import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.sql.expression import func
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resoures={r"/*": {'origins': '*'}})
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,True')
        return response
    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        return jsonify({'success': True, 'categories': [
                       category.format()['type'] for category in categories]})

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions')
    def get_questions():
        q_page = 10
        questions = Question.query.all()
        page = request.args.get('page', 1, int)
        start = (page - 1) * q_page
        end = start + q_page
        paginated_questions = questions[start:end]
        if len(paginated_questions) == 0:
            abort(404)
        return jsonify({
            'questions': [question.format() for question in paginated_questions],
            'total_questions': Question.query.count(),
            'categories': [category.format()['type'] for category in Category.query.all()],
            'current_Category': 0
        })

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.filter(Question.id == id).first()
        if question is None:
            abort(422)
        question.delete()
        return jsonify({
            'success': True,
            'deleted': id
        })

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()
        if 'searchTerm' in body:
            searchTerm = body['searchTerm']
            q_page = 10
            page = request.args.get('page', 1, int)
            start = (page - 1) * q_page
            end = start + q_page
            questions = Question.query.filter(
                Question.question.ilike(
                    '%{}%'.format(searchTerm))).all()
            paginated_questions = questions[start:end]
            if len(paginated_questions) == 0:
                abort(404)

            return jsonify({
                'questions': [question.format() for question in paginated_questions],
                'total_questions': len(questions),
                'current_Category': 0
            })
        else:
            question = body['question']
            answer = body['answer']
            difficulty = body['difficulty']
            category = body['category']
            if question == "" or answer == "" or difficulty == "" or category == "":
                abort(400)
            try:
                question = Question(
                    question=question,
                    answer=answer,
                    category=category,
                    difficulty=difficulty)
                question.insert()
            except:
                abort(400)
            return jsonify({
                'success': True,
                'created': question.id
            })

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    # ===========================done with add_question=======================
    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        categories = Category.query.filter(Category.id == category_id).all()
        questions = Question.query.filter(
            Question.category == category_id).all()
        if len(questions) == 0 or len(categories) == 0:
            abort(404)
        return jsonify({
            'questions': [question.format() for question in questions],
            'total_questions': Question.query.count(),
            'categories': [category.format()['type'] for category in Category.query.all()],
            'current_Category': category_id
        })

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def play():
        body = request.get_json()
        previousQuestions = body['previous_questions']
        quizCategory = body['quiz_category']['id']
        if(quizCategory == 0):
            questions = Question.query.filter(
                ~Question.id.in_(previousQuestions)).order_by(
                func.random()).first()
        else:
            category = Category.query.filter(Category.id == quizCategory).one_or_none()
            if category is None:
                abort(404)
            questions = Question.query.filter(
                Question.category == quizCategory,
                ~Question.id.in_(previousQuestions)).order_by(
                func.random()).first()
        if questions is None:
            return jsonify({
                'question': False,
                'answer': False
            })
        return jsonify({
            'question': questions.format(),
            'answer': questions.answer
        })
    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found__questions(error):
        return{
            'success': False,
            'error': 404,
            'message': 'not found'
        }, 404

    @app.errorhandler(422)
    def not_found__questions(error):
        return{
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }, 422

    @app.errorhandler(400)
    def not_found__questions(error):
        return{
            'success': False,
            'error': 400,
            'message': 'bad request'
        }, 400

    @app.errorhandler(405)
    def not_found__questions(error):
        return{
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }, 405

    @app.errorhandler(500)
    def not_found__questions(error):
        return{
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }, 500
    return app
