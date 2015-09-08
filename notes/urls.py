__author__ = 'Jeezy'

from django.conf.urls import include, url
from notes.forms import MyLoginForm

urlpatterns = [
    url(r"^$", 'notes.views.home', name='home'),
    url(r'^auth/login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'notes/auth/login.html',
            'authentication_form': MyLoginForm,
            'extra_context':
            {
                'title': 'Вход пользователя',
            }
        },
        name='login'),
    url(r'^auth/logout/$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),
    url(r"^auth/register/$", 'notes.views.register', name='register'),
    url(r"^auth/register/success/$", 'notes.views.register_success', name='register_success'),
    url(r"^personal/$", 'notes.views.personal_show', name='personal_show'),
    url(r"^personal/categories/$", 'notes.views.personal_categories', name='personal_categories'),
    url(r"^personal/categories/(?P<category_id>[0-9]+)/delete/$", 'notes.views.personal_categories_delete',
        name='personal_categories_delete'),
    url(r"^personal/edit/$", 'notes.views.personal_edit', name='personal_edit'),
    url(r"^personal/edit/avatar/$", 'notes.views.personal_edit_avatar', name='personal_edit_avatar'),
    url(r"^users/$", 'notes.views.users', name='users'),
    url(r"^users/(?P<username>\w+)/$", 'notes.views.user_show', name='user_show'),
    url(r"^users/(?P<username>\w+)/notes/$", 'notes.views.user_notes', name='user_notes'),
    url(r"^users/(?P<username>\w+)/notes/add/$", 'notes.views.user_notes_modify', name='user_notes_add'),
    url(r"^users/(?P<username>\w+)/notes/(?P<note_id>[0-9]+)/$", 'notes.views.user_notes_show', name='user_notes_show'),
    url(r"^users/(?P<username>\w+)/notes/(?P<note_id>[0-9]+)/edit/$",
        'notes.views.user_notes_modify',
        name='user_notes_edit'),
    url(r"^users/(?P<username>\w+)/notes/(?P<note_id>[0-9]+)/delete/$",
        'notes.views.user_notes_delete',
        name='user_notes_delete'),
    url(r"^users/(?P<username>\w+)/notes/(?P<note_id>[0-9]+)/labels/add/$",
        'notes.views.user_notes_labels_add',
        name='user_notes_labels_add'),
    url(r"^users/(?P<username>\w+)/notes/(?P<note_id>[0-9]+)/labels/(?P<label_id>[0-9]+)/delete/$",
        'notes.views.user_notes_labels_delete',
        name='user_notes_labels_delete'),
]