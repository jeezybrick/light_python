from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
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


def user_notes(request, username):
    if request.method == 'POST':
        form = AddNoteForm(request.POST)
        if form.is_valid():
            first = form.save(commit=False)
            first.user = request.user
            first.save()
            print('LAL')
            return HttpResponseRedirect('/home/')
        else:
            form = AddNoteForm()
            return render(request, 'notes/notes/create.html', {'form': form})
    else:
        user = get_object_or_404(User, username=username)
        notes = user.notes_set.order_by('created_at')
        return render(request, 'notes/notes/index.html', {'notes': notes})


def user_notes_add(request, username):
    if request.method == 'POST':
        form = AddNoteForm(request.POST)
        if form.is_valid():
            first = form.save(commit=False)
            first.user = request.user
            first.save()
            return HttpResponseRedirect('/users/'+username+'/notes/')
    else:
        form = AddNoteForm()

    return render(request, 'notes/notes/create.html', {'form': form})


def user_notes_show(request, username, note_id):
    note = get_object_or_404(Notes, id=note_id)
    return render(request, 'notes/notes/show.html', {'note': note})