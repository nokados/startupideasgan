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
        data = rv.data.decode("utf-8")
        self.assertTrue(re.search(r'idea\d\<\/h2\>', data))
        self.assertTrue(re.search(r'input type="hidden" id="idea_id" value="\d"', data))
        
    def test_get_ideas(self):
        """Ensure that a user can get ideas."""
        rv = self.app.post('/get_ideas', follow_redirects=True)
        data = json.loads((rv.data).decode('utf-8'))
        self.assertIn('ideas', data)
        self.assertEqual([{'text': f'idea{i}', 'id': i+1} for i in range(5)], sorted(data['ideas'], key=lambda x: x['id']))
        
    def test_rate(self):
        """Ensure that rating works."""
        
        # Invalid params
        rv = self.app.post('/rate', data={'field': 'likes'}, follow_redirects=True)
        data = json.loads((rv.data).decode('utf-8'))
        self.assertEqual({'status': 0}, data)
        
        # Invalid field
        rv = self.app.post('/rate', data={'id': 1, 'field': 'herks'}, follow_redirects=True)
        data = json.loads((rv.data).decode('utf-8'))
        self.assertEqual({'status': 0}, data)
        
        # Invalid id
        rv = self.app.post('/rate', data={'id': 100, 'field': 'likes'}, follow_redirects=True)
        data = json.loads((rv.data).decode('utf-8'))
        self.assertEqual({'status': 0}, data)
        
        
        self.assertEqual(0, Idea.query.get(1).likes)
        rv = self.app.post('/rate', data={'id': 1, 'field': 'likes'}, follow_redirects=True)
        data = json.loads((rv.data).decode('utf-8'))
        self.assertEqual({'status': 1}, data)
        self.assertEqual(1, Idea.query.get(1).likes)
        rv = self.app.post('/rate', data={'id': 2, 'field': 'dislikes'}, follow_redirects=True)
        self.assertEqual(1, Idea.query.get(2).dislikes)
        rv = self.app.post('/rate', data={'id': 3, 'field': 'skips'}, follow_redirects=True)
        self.assertEqual(1, Idea.query.get(3).skips)
        rv = self.app.post('/rate', data={'id': 1, 'field': 'likes'}, follow_redirects=True)
        self.assertEqual(2, Idea.query.get(1).likes)
        rv = self.app.post('/rate', data={'id': 1, 'field': 'skips'}, follow_redirects=True)
        self.assertEqual(2, Idea.query.get(1).likes)
        self.assertEqual(0, Idea.query.get(1).dislikes)
        self.assertEqual(1, Idea.query.get(1).skips)


if __name__ == '__main__':
    unittest.main()