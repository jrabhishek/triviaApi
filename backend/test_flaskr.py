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
        self.database_name = "trivia"
        self.database_path = "postgresql://postgres:admin@localhost:5432/trivia"
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
    def test_pagenated_questions(self):
       res = self.client().get('/questions')
       data = json.loads(res.data)
       self.assertEqual(res.status_code,200)
       self.assertTrue(data['questions'])


    def test_search_question(self):
       res = self.client().post('/questions',json={"searchTerm":"f"})
       data = json.loads(res.data)
       self.assertEqual(res.status_code,200)

    @unittest.skip("skiping this test because resouce must be present ")
    def test_delete(self):
       res = self.client().delete('/questions/21')
       data = json.loads(res.data)
       self.assertEqual(res.status_code,200)
       self.assertEqual(data['success'],True)


    def test_addBook(self):
       book ={"question":"what",
               "difficulty":1,
               "answer":"no",
               "category":"3" } 
       res = self.client().post('/add',json=book)
       data = json.loads(res.data)
       self.assertEqual(res.status_code,200)
       self.assertEqual(data['success'],True)

    def test_allCategory(self):
       res = self.client().get('/categories')
       data = json.loads(res.data)
       self.assertEqual(res.status_code,200)
       self.assertEqual(data['success'],True)   


    def test_quizzes(self):
       body = {"quiz_category":{"type": "science", "id": 3},
	            "previous_questions":[4]
                } 
       res = self.client().post('/quizzes',json=body)
       data = json.loads(res.data)
       self.assertEqual(res.status_code,200)
       self.assertTrue(data['question'])   


    def test_404_not_found(self):
       res = self.client().delete('/questions/90l')
       data = json.loads(res.data)
       self.assertEqual(res.status_code,404)
       self.assertEqual(data['success'],False)

    def test_422_not_processable_quize(self):
       res = self.client().post('/quizzes',json={"body":"body"})
       data = json.loads(res.data)
       self.assertEqual(res.status_code,422)
           




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()