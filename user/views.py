from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .decorators import unauthenticated_user, getUser
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import User
from .forms import AccountUpdateForm
from django.urls import reverse_lazy

from django.http import HttpResponse, HttpResponseRedirect


from django.http import HttpResponse


@getUser
@unauthenticated_user
def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('postapp:postlist')
    return render(request, 'user/login.html')


@getUser
@login_required
def userlogout(request):
    response = HttpResponseRedirect(reverse_lazy('post:postlist'))
    response.delete_cookie('userinfo')
    return response


@getUser
@unauthenticated_user
def registrer(request):
    context = {}
    return render(request, 'user/signup.html', context=context)


@getUser
@login_required
def userprofile(request):
    context = {
        'title': request.user.username,
    }
    return render(request, 'user/userprofile.html', context=context)


@getUser
@login_required
def userupdateprofile(request):
    context = {
        'title': request.user.username,
    }
    return render(request, 'user/userupdateprofile.html', context=context)
