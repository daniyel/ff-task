import unittest
import json

from main.app import app
from main.db import db

TEST_DB = '/tmp/test.db'

db.init_app(app)


class SearchPlateTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB
        self.app = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        pass

    # TESTS
    def test_search_plate(self):
        self.app.post(
            '/plate',
            data=json.dumps(dict(plate='A-BC123')),
            content_type='application/json',
            follow_redirects=True
        )
        self.app.post(
            '/plate',
            data=json.dumps(dict(plate='A-CC123')),
            content_type='application/json',
            follow_redirects=True
        )
        self.app.post(
            '/plate',
            data=json.dumps(dict(plate='A-CC123')),
            content_type='application/json',
            follow_redirects=True
        )

        response = self.app.get(
            '/search-plate?key=ABC123&levenshtein=1',
            follow_redirects=True
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['ABC123']), 3)


if __name__ == "__main__":
    unittest.main()
