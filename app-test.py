from app import app, db
import os, re
import json
from models import Idea

import unittest

TEST_DB = 'test.db'

class BasicTestCase(unittest.TestCase):

    def test_index(self):
        """initial test. ensure flask was set up correctly"""
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        
    def test_database(self):
        """initial test. ensure that the database exists"""
        tester = os.path.exists('flaskr.db')
        self.assertEqual(tester, True)

class FlaskrTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up a temp database before each test"""
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['TESTING'] = True
        self.test_db_path = os.path.join(basedir, TEST_DB)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.test_db_path
        self.app = app.test_client()
        db.create_all()
        fixtures = [Idea(text=f'idea{i}') for i in range(5)]
        db.session.bulk_save_objects(fixtures)
        db.session.commit()
    
    def tearDown(self):
        """Destroy blank temp database after each test"""
        db.drop_all()
        os.remove(self.test_db_path)
    
    def test_index(self):
        """Ensure that a main view shows an idea within <h1></h1>"""
        rv = self.app.get('/')
        self.assertTrue(re.search(r'idea\d\<\/h1\>', rv.data.decode("utf-8")))
        
    def test_get_ideas(self):
        """Ensure that a user can get ideas."""
        rv = self.app.post('/get_ideas', follow_redirects=True)
        data = json.loads((rv.data).decode('utf-8'))
        self.assertIn('ideas', data)
        self.assertEqual([f'idea{i}' for i in range(5)], sorted(data['ideas']))

if __name__ == '__main__':
    unittest.main()