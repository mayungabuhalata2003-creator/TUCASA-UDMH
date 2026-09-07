import unittest

from app import create_app
from models import ChatMessage, EventPost, Publication, User


class AdminMediaFeaturesTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_admin_choir_dashboard_exists(self):
        with self.app.app_context():
            user = User.query.filter_by(email='admin@tucasa.ac.tz').first()
            self.assertIsNotNone(user)

        response = self.client.get('/admin/kwaya')
        self.assertNotEqual(response.status_code, 404)

    def test_event_and_publication_models_exist(self):
        with self.app.app_context():
            self.assertTrue(hasattr(EventPost, '__tablename__'))
            self.assertTrue(hasattr(Publication, '__tablename__'))

    def test_chat_requires_login(self):
        response = self.client.get('/chat')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_chat_message_model_exists(self):
        with self.app.app_context():
            self.assertEqual(ChatMessage.__tablename__, 'chat_messages')
            self.assertTrue(hasattr(ChatMessage, 'sender'))


if __name__ == '__main__':
    unittest.main()
