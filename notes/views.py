from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import MyUser, Notes, ColorOfNote, Category
from .forms import MyRegForm, ModifyNoteForm, EditProfileForm, AddLabelForm, EditAvatarForm, AddCategory
from PIL import Image


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


@login_required(login_url='/auth/login/')
def user_show(request, username):
    user = get_object_or_404(MyUser, username=username)
    return render(request, 'notes/users/show.html', {'user': user})


@login_required(login_url='/auth/login/')
def user_notes(request, username):

        user_owner = get_object_or_404(MyUser, username=username)
        if user_owner.username == request.user.username or not user_owner.is_private:
            pass
        else:
            raise Exception('Этот пользователь закрыл свои заметки.')
        notes = user_owner.notes_set.order_by('-created_at')
        paginator = Paginator(notes, 6)  # Show 6 contacts per page
        page = request.GET.get('page')
        try:
            notes = paginator.page(page)
        except PageNotAnInteger:
            notes = paginator.page(1)
        except EmptyPage:
            # raise Http404("Новости с таким адресом не существует")
            notes = paginator.page(paginator.num_pages)
        return render(request, 'notes/notes/index.html', {'notes': notes, 'user_owner': user_owner})


@login_required(login_url='/auth/login/')
def user_notes_show(request, username, note_id):
    user_owner = get_object_or_404(MyUser, username=username)
    note = get_object_or_404(Notes, id=note_id)
    if user_owner.username == request.user.username or not user_owner.is_private:
        pass
    else:
        raise Exception('Этот пользователь закрыл свои заметки.')
    return render(request, 'notes/notes/show.html', {'note': note})


@login_required(login_url='/auth/login/')
def user_notes_modify(request, username, note_id=None):
    if note_id is not None:
        try:
            note = request.user.notes_set.get(id=note_id)
        except:
            raise Exception('Вы пытаетесь редактировать заметку другому пользователю?')
        foo = 'Редактировать'
    else:
        user_owner = get_object_or_404(MyUser, username=username)
        if not user_owner.username == request.user.username:
            raise Exception('Вы пытаетесь добавить заметку другому пользователю?')
        note = None
        foo = 'Добавить'
    if request.method == 'POST':
        print(request.POST)
        form = ModifyNoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            first = form.save(commit=False)
            first.user = request.user
            first.save()
            form.save_m2m()
            return HttpResponseRedirect('/users/'+username+'/notes/'+str(first.id)+'/')
        return render(request, 'notes/notes/modify.html', {'form': form, 'note': note})
    else:
        form = ModifyNoteForm(instance=note)

    return render(request, 'notes/notes/modify.html', {'note': note, 'form': form,
                                                       'foo': foo})


@login_required(login_url='/auth/login/')
def user_notes_delete(request, username, note_id):
    if request.method == 'POST':
        user_owner = get_object_or_404(MyUser, username=username)
        if not user_owner.username == request.user.username:
            raise Exception('Вы пытаетесь удалить заметку другому пользователю?')
        note = get_object_or_404(Notes, id=note_id)
        note.delete()
    return HttpResponseRedirect('/users/'+username+'/notes')


@login_required(login_url='/auth/login/')
def personal_show(request):
    return render(request, 'notes/personal/index.html')


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


@login_required(login_url='/auth/login/')
def user_notes_labels_add(request, username, note_id):
    if request.method == 'POST':
        form = AddLabelForm(request.POST, request.FILES)
        if form.is_valid():
            note = request.user.notes_set.get(id=note_id)
            first = form.save(commit=False)
            first.note = note
            first.save()
            return HttpResponseRedirect('/users/'+request.user.username+'/notes/')
    else:
        form = AddLabelForm()
    return render(request, 'notes/labels/add.html', {'form': form})


@login_required(login_url='/auth/login/')
def personal_edit_avatar(request):
    if request.method == 'POST':
        form = EditAvatarForm(request.POST, request.FILES, instance=request.user)
        request.FILES['avatar'].name = str(request.user.username) + request.FILES['avatar'].name[-4:]
        if form.is_valid():
            form.save()
            messages.success(request, 'Аватар успешно загружен!')
            return HttpResponseRedirect('/personal/')
    else:
        form = EditAvatarForm(instance=request.user)
    return render(request, 'notes/users/avatar.html', {'form': form})


@login_required(login_url='/auth/login/')
def personal_categories(request):
    if request.method == 'POST':
        try:
            request.POST["parent"]
        except:
            raise Exception('Вы не ввели значение для главной категории!')
        parent = Category(name=request.POST["parent"], user_id=request.user.id)
        parent.save()
        callback = 'Категория добалена!'
        for value in request.POST.getlist("child"):
            child = Category(name=value, parent_category_id=parent.id, user_id=request.user.id)
            child.save()
            callback = 'Категории добалены!'
        messages.success(request, callback)
        return HttpResponseRedirect('/personal/')
    else:
        parent_note = request.user.category_set.filter(parent_category_id__isnull=True)
    return render(request, 'notes/personal/categories.html', {'parent_note': parent_note})


@login_required(login_url='/auth/login/')
def personal_categories_delete(request, category_id):
    try:
        category = request.user.category_set.get(id=category_id)
    except:
        raise Exception('Вы пытаетесь редактировать заметку другому пользователю?')
    category.delete()
    return HttpResponseRedirect('/personal/')