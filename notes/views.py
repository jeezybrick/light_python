from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import MyRegForm
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