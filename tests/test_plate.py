import unittest
import json

from main.app import app
from main.db import db

TEST_DB = '/tmp/test.db'

db.init_app(app)


class PlateTests(unittest.TestCase):
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
    def test_missing_plate_field(self):
        response = self.app.post(
            '/plate',
            data=json.dumps({}),
            content_type='application/json',
            follow_redirects=True
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Field plate is missing.')

    def test_invalid_german_plate(self):
        response = self.app.post(
            '/plate',
            data=json.dumps(dict(plate='A-BC12345')),
            content_type='application/json',
            follow_redirects=True
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            data['message'],
            'Field plate is not valid German plate.')

    def test_create_plate(self):
        response = self.app.post(
            '/plate',
            data=json.dumps(dict(plate='A-BC123')),
            content_type='application/json',
            follow_redirects=True
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['plate'], 'A-BC123')
        self.assertIn('timestamp', data.keys())

    def test_get_plates(self):
        response = self.app.get('/plate', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data))


if __name__ == "__main__":
    unittest.main()
