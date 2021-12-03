from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .decorators import unauthenticated_user
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import User
from .forms import  AccountUpdateForm
from django.urls import reverse_lazy


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

@login_required
def userlogout(request):
    request.user.auth_token.delete()
    logout(request)
    return redirect('login')

@unauthenticated_user
def registrer(request):
    context = {}
    return render(request, 'user/signup.html', context=context)


@login_required
def userprofile(request):
    context = {
        'title': request.user.username,
    }
    return render(request, 'user/userprofile.html', context=context)

@login_required
def userupdateprofile(request):
    context = {
        'title': request.user.username,
    }
    return render(request, 'user/userupdateprofile.html', context=context)

# class UserProfileUpdate(generic.UpdateView, LoginRequiredMixin):
#     model = User
#     form_class = AccountUpdateForm
#     success_url = reverse_lazy('profile')

#     def get_object(self):
#         return User.objects.get(pk=self.request.user.pk)
