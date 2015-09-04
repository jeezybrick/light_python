from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User, Notes
from .forms import MyRegForm, AddNoteForm
# Create your views here.


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
    users_list = User.objects.order_by('id')
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
def user_notes(request, username):
    if request.method == 'POST':
        form = AddNoteForm(request.POST)
        if form.is_valid():
            first = form.save(commit=False)
            first.user = request.user
            first.save()
            form.save_m2m()
            # first.tags.add(*form.cleaned_data['tags'])
            return HttpResponseRedirect('/users/'+username+'/notes/')
        else:
            return render(request, 'notes/notes/modify.html', {'form': form})
    else:
        user_owner = get_object_or_404(User, username=username)
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
            # If page is not an integer, deliver first page.
            notes = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            # raise Http404("Новости с таким адресом не существует")
            notes = paginator.page(paginator.num_pages)
        return render(request, 'notes/notes/index.html', {'notes': notes, 'user_owner': user_owner})



@login_required(login_url='/auth/login/')
def user_notes_show(request, username, note_id):
    user_owner = get_object_or_404(User, username=username)
    note = get_object_or_404(Notes, id=note_id)
    if user_owner.username == request.user.username or not user_owner.is_private:
        pass
    else:
        raise Exception('Этот пользователь закрыл свои заметки.')
    if request.method == 'POST':
        form = AddNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/users/'+request.user.username+'/notes/'+note_id+'/')
        else:
            return render(request, 'notes/notes/modify.html', {'form': form, 'note': note})
    else:
        return render(request, 'notes/notes/show.html', {'note': note})


@login_required(login_url='/auth/login/')
def user_notes_modify(request, username, note_id=None):
    if note_id is not None:
        try:
            note = request.user.notes_set.get(id=note_id)
        except:
            raise Exception('Вы пытаетесь добавить или редактировать заметку другому пользователю?')
        foo = 'Редактирование'
    else:
        user_owner = get_object_or_404(User, username=username)
        if not user_owner.username == request.user.username:
            raise Exception('Вы пытаетесь добавить или редактировать заметку другому пользователю?')
        note = None
        foo = 'Добавление'

    if request.method == 'POST':
        form = AddNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/users/'+username+'/notes/'+note_id+'/')
        return render(request, 'notes/notes/modify.html', {'form': form, 'note': note})
    else:
        form = AddNoteForm(instance=note)

    return render(request, 'notes/notes/modify.html', {'note': note, 'form': form, 'foo': foo})