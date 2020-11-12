import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format(
            'safaa:5433116@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # 1

    def test_pagination_of_questions_successful(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])
        self.assertIsNotNone(data['categories'])
        self.assertIsNotNone(data['current_Category'])
    # 2

    def test_404_pagination_of_questions_failed(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')
    # 3

    # def test_delete_question_successful(self):
    #     res = self.client().delete('/questions/2')
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(data['deleted'], 2)
    # 4

    def test_422_delete_question_failed(self):
        res = self.client().delete('/questions/6000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')

    # 5
    def test_search_questions_successful(self):
        res = self.client().post('/questions', json={'searchTerm': 'a'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])
    # 6

    def test_404_search_questions_empty(self):
        res = self.client().post('/questions',
                                 json={'searchTerm': 'zzzzzzzzzzzzzzzzzzz'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')
    # 7

    def test_add_questions_successful(self):
        res = self.client().post(
            '/questions',
            json={
                'question': 'this is you?',
                'answer': 'yes',
                'difficulty': 4,
                'category': 3})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['created'])
    # 8

    def test_400_add_questions_failed(self):
        res = self.client().post(
            '/questions',
            json={
                'question': '',
                'answer': 'yes',
                'difficulty': 4,
                'category': 3})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')
    # 9

    def test_400_add_questions_category_failed(self):
        res = self.client().post(
            '/questions',
            json={
                'question': 'xxx',
                'answer': 'ans',
                'difficulty': 4,
                'category': 300})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')
    # 10

    def test_get_questions_by_category_successful(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])
        self.assertIsNotNone(data['categories'])
        self.assertIsNotNone(data['current_Category'])
    # 11

    def test_get_questions_by_category_failed(self):
        res = self.client().get('/categories/2000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')
    # 12

    def test_quiz_successful_for_Science_category(self):
        res = self.client().post(
            '/quizzes',
            json={
                'previous_questions': '',
                'quiz_category': {
                    'id': 1,
                    'type': 'Science'}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['question'])
        self.assertIsNotNone(data['answer'])
    # 13

    def test_quiz_successful_for_all_categories(self):
        res = self.client().post(
            '/quizzes',
            json={
                'previous_questions': '',
                'quiz_category': {
                    'id': '0',
                    'type': 'click'}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['question'])
        self.assertIsNotNone(data['answer'])
    # 14

    def test_quiz_successful_for_unexisting_categories(self):
        res = self.client().post(
            '/quizzes',
            json={
                'previous_questions': '',
                'quiz_category': {
                    'id': 5000,
                    'type': 'click'}})
        data = json.loads(res.data)
        self.assertFalse(data['question'])


if __name__ == "__main__":
    unittest.main()
