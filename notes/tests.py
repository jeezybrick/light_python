import unittest
from django.test import Client
from django.contrib.auth.models import User
from .models import Notes
from django.http import request
from django.shortcuts import render, get_object_or_404


class SimpleTest(unittest.TestCase):
    def setUp(self):
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        user_two = User.objects.create_user('temporary2', 'temporary2@gmail.com', 'temporary')
        # note = Notes.objects.objects.order_by('id')
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

    def test_logout(self):
        response = self.client.get('/auth/logout/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_users(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_users_notes(self):
        user = User.objects.get(username='temporary')
        response = self.client.get('/users/john/notes/')
        self.assertEqual(response.status_code, 302)
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/users/'+user.username+'/notes/')
        self.assertEqual(response.status_code, 200)

    def test_users_notes_add(self):
        user = User.objects.get(username='temporary')
        response = self.client.get('/users/'+user.username+'/notes/add/')
        self.assertEqual(response.status_code, 302)
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/users/'+user.username+'/notes/add/')
        self.assertEqual(response.status_code, 200)
