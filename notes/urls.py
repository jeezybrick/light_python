__author__ = 'Jeezy'

from django.conf.urls import include, url
from notes.forms import BootstrapAuthenticationForm

urlpatterns = [
    url(r"^$", 'notes.views.home', name='home'),
    url(r'^auth/login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'notes/auth/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),
    url(r"^auth/register/$", 'notes.views.register', name='register'),
    url(r"^auth/register/success/$", 'notes.views.register_success', name='register_success'),
    url(r"^users/(?P<username>\w+)/notes/$", 'notes.views.user_notes', name='user_notes'),
    url(r"^users/(?P<username>\w+)/notes/add/$", 'notes.views.user_notes_add', name='user_notes_add'),
    url(r"^users/(?P<username>\w+)/notes/(?P<note_id>[0-9]+)/$", 'notes.views.user_notes_show', name='user_notes_show'),
]