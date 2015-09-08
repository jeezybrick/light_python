from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import MyUser, Note, Category, LabelCustom
from .forms import MyRegForm, ModifyNoteForm, EditProfileForm, AddLabelForm, EditAvatarForm


def home(request):
    return render(request, 'notes/home.html')


def register(request):
    if request.method == 'POST':
        form = MyRegForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/auth/register/success')
    else:
        form = MyRegForm()

    return render(request, 'notes/auth/register.html', {'form': form})


def register_success(request):
    return render(request, 'notes/auth/register_success.html')


# Список пользователей
def users(request):
    users_list = MyUser.objects.order_by('id')
    paginator = Paginator(users_list, 2)
    page = request.GET.get('page')
    try:
        users_list = paginator.page(page)
    except PageNotAnInteger:
        users_list = paginator.page(1)
    except EmptyPage:
        users_list = paginator.page(paginator.num_pages)
    return render(request, 'notes/users/index.html', {'users_list': users_list})


# Вывод информации о пользователе
@login_required(login_url='/auth/login/')
def user_show(request, username):
    user = get_object_or_404(MyUser, username=username)
    return render(request, 'notes/users/show.html', {'user': user})


# Вывод списка заметок выбранного пользователя
@login_required(login_url='/auth/login/')
def user_notes(request, username):
    user_owner = get_object_or_404(MyUser, username=username)
    """
    Список заметок будет показан если пользователь является автором заметки или
    если он открыл их для общего доступа
    """
    if user_owner.username == request.user.username or not user_owner.is_private:
        pass
    else:
        raise Exception('Этот пользователь закрыл свои заметки.')

    # Проверяем если ли у выбранного пользователя созданные заметки
    try:
        notes = user_owner.note_set.order_by('-created_at')
    except AttributeError:
        notes = None
    else:
        paginator = Paginator(notes, 6)
        page = request.GET.get('page')
        try:
            notes = paginator.page(page)
        except PageNotAnInteger:
            notes = paginator.page(1)
        except EmptyPage:
            notes = paginator.page(paginator.num_pages)
    return render(request, 'notes/notes/index.html', {'notes': notes, 'user_owner': user_owner})


# Вывод детальной информации о заметке
@login_required(login_url='/auth/login/')
def user_notes_show(request, username, note_id):
    user_owner = get_object_or_404(MyUser, username=username)
    note = get_object_or_404(Note, id=note_id)
    # Заметка будет показана если пользователь является автором заметки или если он открыл их для общего доступа
    if user_owner.username == request.user.username or not user_owner.is_private:
        pass
    else:
        raise Exception('Этот пользователь закрыл свои заметки.')
    return render(request, 'notes/notes/show.html', {'note': note})


# Создание или удаление заметки
@login_required(login_url='/auth/login/')
def user_notes_modify(request, username, note_id=None):
    """
    Если в url была id заметки проверяем является ли пользователь автором заметки
    Также заносим в переменную обьект заметки для ее редактирования
    """
    if note_id is not None:
        try:
            note = request.user.note_set.get(id=note_id)
        except:
            raise Exception('Вы пытаетесь редактировать заметку другому пользователю?')
        foo = 'Редактировать'
    # Создаем форму для редактирвоания или создания заметки.Проверяем владельца
    else:
        user_owner = get_object_or_404(MyUser, username=username)
        if not user_owner.username == request.user.username:
            raise Exception('Вы пытаетесь добавить заметку другому пользователю?')
        note = None
        foo = 'Добавить'
    if request.method == 'POST':
        form = ModifyNoteForm(request.user, request.POST, request.FILES, instance=note)
        if form.is_valid():
            first = form.save(commit=False)
            first.user = request.user
            first.save()
            form.save_m2m()
            return HttpResponseRedirect('/users/' + username + '/notes/' + str(first.id) + '/')
        return render(request, 'notes/notes/modify.html', {'form': form, 'note': note})
    else:
        form = ModifyNoteForm(instance=note, user=request.user)

    return render(request, 'notes/notes/modify.html', {'note': note, 'form': form,
                                                       'foo': foo})


# Удаление заметки
@login_required(login_url='/auth/login/')
def user_notes_delete(request, username, note_id):
    if request.method == 'POST':
        user_owner = get_object_or_404(MyUser, username=username)
        if not user_owner.username == request.user.username:
            raise Exception('Вы пытаетесь удалить заметку другому пользователю?')
        note = get_object_or_404(Note, id=note_id)
        note.delete()
    return HttpResponseRedirect('/users/' + username + '/notes')


# Личный кабинет
@login_required(login_url='/auth/login/')
def personal_show(request):
    return render(request, 'notes/personal/index.html')


# Редактирование личной информации пользателя
@login_required(login_url='/auth/login/')
def personal_edit(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Личные данные успешно отредактированы!')
            return HttpResponseRedirect('/personal/')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'notes/personal/edit.html', {'form': form})


# Создание собственных ярлыков
@login_required(login_url='/auth/login/')
def user_notes_labels_add(request, username, note_id):
    user_owner = get_object_or_404(MyUser, username=username)
    if not user_owner.username == request.user.username:
        raise Exception('Доступ запрещен')
    if request.method == 'POST':
        form = AddLabelForm(request.POST, request.FILES)
        if form.is_valid():
            note = request.user.note_set.get(id=note_id)
            first = form.save(commit=False)
            first.note = note
            first.save()
            messages.success(request, 'Ярлык добавлен!')
            return HttpResponseRedirect('/users/' + request.user.username + '/notes/' + note_id + '/')
    else:
        form = AddLabelForm()
    return render(request, 'notes/labels/add.html', {'form': form})


# Удаление собственного ярлыка
@login_required(login_url='/auth/login/')
def user_notes_labels_delete(request, username, note_id, label_id):
    try:
        note = request.user.note_set.get(id=note_id)
    except:
        raise Exception('Вы пытаетесь удалить значок другого пользователя?')
    label = get_object_or_404(LabelCustom, id=label_id)
    label.delete()
    messages.success(request, 'Ярлык удален!')
    return HttpResponseRedirect('/users/' + request.user.username + '/notes/' + note_id + '/')


# Загрузка и редактирование аватарки
@login_required(login_url='/auth/login/')
def personal_edit_avatar(request):
    if request.method == 'POST':
        form = EditAvatarForm(request.POST, request.FILES, instance=request.user)
        # Делаем имя аватарки как логин у пользователя
        request.FILES['avatar'].name = str(request.user.username) + request.FILES['avatar'].name[-4:]
        if form.is_valid():
            form.save()
            messages.success(request, 'Аватар успешно загружен!')
            return HttpResponseRedirect('/personal/')
    else:
        form = EditAvatarForm(instance=request.user)
    return render(request, 'notes/users/avatar.html', {'form': form})


# Создание и удаление категорий пользователя
@login_required(login_url='/auth/login/')
def personal_categories(request):
    if request.method == 'POST':
        # Ошибка если пользователь не указал родительскую категорию
        try:
            request.POST["parent"]
        except:
            raise Exception('Вы не ввели значение для главной категории!')
        # Создаем новый обьект и сохраняем его
        parent = Category(name=request.POST["parent"], user_id=request.user.id)
        parent.save()
        callback = 'Категория добалена!'
        # Перебираем список дочерних категорий,создаем и сохраняем их обьекты
        for value in request.POST.getlist("child"):
            child = Category(name=value, parent_category_id=parent.id, user_id=request.user.id)
            child.save()
            callback = 'Категории добалены!'
        messages.success(request, callback)
        return HttpResponseRedirect('/personal/')
    else:
        parent_note = request.user.category_set.filter(parent_category_id__isnull=True)
    return render(request, 'notes/personal/categories.html', {'parent_note': parent_note})


# Удаление категорий
@login_required(login_url='/auth/login/')
def personal_categories_delete(request, category_id):
    try:
        category = request.user.category_set.get(id=category_id)
    except:
        raise Exception('Вы пытаетесь удалить категорию другому пользователю?')
    category.delete()
    messages.success(request, 'Категория удалена!')
    return HttpResponseRedirect('/personal/categories/')
