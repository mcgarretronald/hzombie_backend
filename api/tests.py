from django.test import TestCase
from users.models import User
from script.models import Script
from ratings.models import Rating

class UserModelTests(TestCase):
    def test_create_user_successful(self):
        user = User.objects.create_user(email='test@example.com', password='testpass')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass'))

class ScriptModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='author@example.com', password='password123')
        self.script_data = {
            'title': 'Sample Script',
            'synopsis': 'This is a sample script synopsis.',
            'user': self.user,
        }
        self.script = Script.objects.create(**self.script_data)

    def test_script_creation(self):
        self.assertIsInstance(self.script, Script)
        self.assertEqual(self.script.title, 'Sample Script')
        self.assertEqual(self.script.synopsis, 'This is a sample script synopsis.')

    def test_script_string_representation(self):
        self.assertEqual(str(self.script), 'Sample Script')
