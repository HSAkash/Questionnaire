from django.http import HttpResponse
from django.shortcuts import redirect
from .models import User

from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from django.contrib.auth.models import AnonymousUser


def unauthenticated_user(view_func):

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('post:postlist')
        return view_func(request, *args, **kwargs)
    return wrapper_func


def getUser(view_func):

    def wrapper_func(request, *args, **kwargs):
        request.user = AnonymousUser()
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1] if \
            request.META.get('HTTP_AUTHORIZATION') else (request.COOKIES.get(
                'userinfo').split(' ')[1] if request.COOKIES.get(
                'userinfo') else None)
        data = {'token': token}
        try:
            valid_data = TokenVerifySerializer().validate(data)
            valid_data = TokenBackend(
                algorithm='HS256').decode(token, verify=False)
            user = User.objects.get(pk=valid_data['user_id'])
            request.user = user
        except Exception as v:
            # print("validation error", v)
            pass
        return view_func(request, *args, **kwargs)
    return wrapper_func
