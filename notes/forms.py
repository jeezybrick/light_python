__author__ = 'Jeezy'

"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.forms.extras.widgets import SelectDateWidget
from django.core import validators
from .models import Notes, MyUser, Category
from .widgets import MyWidgetForColor, MyWidgetForLabels
MEDIA_CHOICES = (
        ('Audio', (
            ('vinyl', 'Vinyl'),
            ('cd', 'CD'),
        )
         ),
        ('Video', (
            ('vhs', 'VHS Tape'),
            ('dvd', 'DVD'),
        )
         ),
)

class MyLoginForm(AuthenticationForm):

    username = forms.CharField(label='Логин', max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Введите ваш логин'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Введите ваш пароль'}))


class MyRegForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Пароли не совпадают!",
    }
    username = forms.CharField(help_text='Максимум 30 символов',
                               validators=[
                                   validators.RegexValidator(r'^[\w.@+-]+$',
                                                             'Введите правильный логин. '
                                                             'Логин может состоять из букв,цифр'
                                                             'и  @/./+/-/_ символов.',
                                                             'invalid'),
                                   ],
                               error_messages={'required': 'Это поле обязательное к запонению',
                                               'unique': 'Пользователь с таким логином уже существует'}
                               )
    password1 = forms.CharField(min_length=6, label='Пароль', widget=forms.PasswordInput,
                                help_text="Минимум 6 символов",)
    password2 = forms.CharField(min_length=6, label='Введите пароль еще раз',
                                help_text="Введите повторно пароль для проверки",
                                widget=forms.PasswordInput)
    last_name = forms.CharField(max_length=50, label='Фамилия',
                                error_messages={'required': 'Это поле обязательное к запонению'})
    first_name = forms.CharField(max_length=50, label='Имя',
                                 error_messages={'required': 'Это поле обязательное к запонению'})
    email = forms.EmailField(label='Email', required=True,
                             error_messages={'unique': 'Пользователь с таким email уже существует'})
    phone = forms.CharField(max_length=30, label='Телефон',
                            help_text='Телефон в формате ***-*******',
                            validators=[
                                validators.RegexValidator(r'^\d{3}\-\d{7}$',
                                                          'Введите телефон в правильном формате!(***-*******)',
                                                          'invalid'), ])
    date_of_birth = forms.DateField(label='Дата рождения', required=True,
                                    widget=SelectDateWidget(empty_label="Nothing"),
                                    error_messages={'invalid': 'Неверный формат даты'})

    class Meta:
        model = MyUser
        fields = ('last_name', 'first_name', 'username', 'email', 'password1', 'password2', 'date_of_birth', 'phone')

    def save(self, commit=True):
        user = super(MyRegForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


def categories_as_choices():
    categories = []
    for category in Category.objects.filter(parent_category_id__isnull=True):
        new_category = []
        sub_categories = []
        for sub_category in category.category_set.all():
            sub_categories.append([sub_category.id, sub_category.name])

        new_category = [category.name, sub_categories]
        categories.append(new_category)

    return categories


class ModifyNoteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModifyNoteForm, self).__init__(*args, **kwargs)

    message = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'cols': 20, 'rows': 5}))
    categories = forms.MultipleChoiceField(required=False,
                                           choices=categories_as_choices())

    class Meta:
        model = Notes
        fields = ('title', 'message', 'color', 'categories', 'labels', )
        widgets = {
            # 'categories': forms.CheckboxSelectMultiple(attrs={'class': 'lal'}),
            'labels': MyWidgetForLabels(attrs={'class': 'label_picker'}),
            # 'color': MyWidgetForColor(),
        }


class EditProfileForm(forms.ModelForm):

    date_of_birth = forms.DateField(label='Дата рождения', required=True,
                                    widget=SelectDateWidget(empty_label="Nothing"))

    class Meta:
        model = MyUser
        fields = ('last_name', 'first_name', 'username', 'email', 'date_of_birth', 'phone', 'is_private', )
        exclude = ('password',)