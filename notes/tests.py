import unittest
from django.test import Client


class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_get(self):
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_post(self):
        response = self.client.post('/auth/login/', {'username': 'john', 'password': 'smith'})
        self.assertEqual(response.status_code, 200)

    def test_register_get(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_post(self):
        response = self.client.post('/auth/register/', {'username': 'john', 'password': 'smith'})
        self.assertEqual(response.status_code, 200)

    def test_users(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_users_notes(self):
        response = self.client.get('/users/john/notes/')
        self.assertEqual(response.status_code, 404)

    def test_users_notes_show(self):
        response = self.client.get('/users/john/notes/1/')
        self.assertEqual(response.status_code, 404)