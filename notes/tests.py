from django.test import Client, TestCase
from .models import MyUser, Category, Notes

"""
Тесты для првоерки:
1.Get и Post запросов к view
2.Кодов HTTP-ответов для авторизированыых пользователей и для анонимусов
3.Exception при попытке действий над обьектами другого пользователя
"""


class SimpleTest(TestCase):
    def setUp(self):
        self.user1 = MyUser.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.user2 = MyUser.objects.create_user('temporary2', 'temporaryrr@gmail.com', 'temporary')
        self.notes = Notes.objects.order_by('id')
        self.categories = Category.objects.order_by('id')
        self.category = Category(name='temporary', user_id=1)
        self.client = Client()

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()

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

    def test_personal(self):
        response = self.client.get('/personal/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/personal/')
        self.assertEqual(response.status_code, 200)

    def test_personal_categories(self):
        response = self.client.get('/personal/categories/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/personal/categories/')
        self.assertEqual(response.status_code, 200)

    def test_personal_categories_delete(self):
        self.client.login(username='temporary', password='temporary')
        category = Category(name='temporary', user_id=self.user1.id)
        category.save()
        response = self.client.get('/personal/categories/'+str(category.id)+'/delete/', follow=True)
        self.assertEqual(response.status_code, 200)

        self.client.login(username='temporary2', password='temporary')
        category = Category(name='temporary', user_id=self.user1.id)
        category.save()
        with self.assertRaisesMessage(Exception, 'Вы пытаетесь удалить категорию другому пользователю?'):
            self.client.get('/personal/categories/'+str(category.id)+'/delete/')

    def test_personal_edit(self):
        response = self.client.get('/personal/edit/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/personal/edit/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/personal/edit/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_users(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)

    def test_users_notes(self):
        response = self.client.get('/users/'+self.user1.username+'/notes/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/users/'+self.user1.username+'/notes/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        self.client.login(username='temporary2', password='temporary')
        with self.assertRaisesMessage(Exception, 'Этот пользователь закрыл свои заметки.'):
            self.client.get('/users/'+self.user1.username+'/notes/')

    def test_users_notes_modify(self):
        response = self.client.get('/users/'+self.user1.username+'/notes/add/')
        self.assertEqual(response.status_code, 302)

        note = Notes(title='temporary', message='message', color_id='2', user_id=self.user1.id)
        note.save()
        fake_note_id = 9999
        fake_user_username = 'fake_username'
        response = self.client.get('/users/'+self.user1.username+'/notes/'+str(note.id)+'/edit/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/users/'+self.user1.username+'/notes/add/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/users/'+self.user1.username+'/notes/'+str(note.id)+'/edit/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/users/'+self.user1.username+'/notes/add/', follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/users/'+fake_user_username+'/notes/add/', follow=True)
        self.assertEqual(response.status_code, 404)

        response = self.client.post('/users/'+self.user1.username+'/notes/'+str(note.id)+'/edit/', follow=True)
        self.assertEqual(response.status_code, 200)

        self.client.login(username='temporary2', password='temporary')
        with self.assertRaisesMessage(Exception, 'Вы пытаетесь добавить заметку другому пользователю?'):
            self.client.post('/users/'+self.user1.username+'/notes/add/')

        with self.assertRaisesMessage(Exception, 'Вы пытаетесь редактировать заметку другому пользователю?'):
            self.client.post('/users/'+self.user1.username+'/notes/'+str(note.id)+'/edit/')

    def test_users_notes_show(self):
        note = Notes(title='temporary', message='message', color_id='2', user_id=self.user1.id)
        note.save()
        response = self.client.get('/users/'+self.user1.username+'/notes/'+str(note.id)+'/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/users/'+self.user1.username+'/notes/'+str(note.id)+'/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        self.client.login(username='temporary2', password='temporary')
        with self.assertRaisesMessage(Exception, 'Этот пользователь закрыл свои заметки.'):
            self.client.post('/users/'+self.user1.username+'/notes/'+str(note.id)+'/')

    def test_users_notes_delete(self):
        note = Notes(title='temporary', message='message', color_id='2', user_id=self.user1.id)
        note.save()
        fake_note_id = 9999
        fake_user_id = 9999
        response = self.client.get('/users/'+self.user1.username+'/notes/'+str(note.id)+'/delete/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/users/'+self.user1.username+'/notes/'+str(note.id)+'/delete/')
        self.assertEqual(response.status_code, 302)

        response = self.client.post('/users/'+self.user1.username+'/notes/'+str(fake_note_id)+'/delete/', follow=True)
        self.assertEqual(response.status_code, 404)

        response = self.client.post('/users/'+self.user1.username+'/notes/'+str(fake_user_id)+'/delete/', follow=True)
        self.assertEqual(response.status_code, 404)

        response = self.client.post('/users/'+self.user1.username+'/notes/'+str(note.id)+'/delete/', follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/users/'+self.user1.username+'/notes/'+str(note.id)+'/delete/')
        self.assertEqual(response.status_code, 404)
        self.client.logout()

        self.client.login(username='temporary2', password='temporary')
        note = Notes(title='temporary', message='message', color_id='2', user_id=self.user1.id)
        note.save()
        with self.assertRaisesMessage(Exception, 'Вы пытаетесь удалить заметку другому пользователю?'):
            self.client.post('/users/'+self.user1.username+'/notes/'+str(note.id)+'/delete/')

    def test_user_notes_labels_add(self):

        note = Notes(title='temporary', message='message', color_id='2', user_id=self.user1.id)
        note.save()
        response = self.client.get('/users/'+self.user1.username+'/notes/'+str(note.id)+'/labels/add/')
        self.assertEqual(response.status_code, 302)

        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/users/'+self.user1.username+'/notes/'+str(note.id)+'/labels/add/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/users/'+self.user1.username+'/notes/'+str(note.id)+'/labels/add/',
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        self.client.login(username='temporary2', password='temporary')
        with self.assertRaisesMessage(Exception, 'Доступ запрещен'):
            self.client.post('/users/'+self.user1.username+'/notes/'+str(note.id)+'/labels/add/', follow=True)