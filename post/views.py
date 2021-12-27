from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from post import models as post_models
from user import models as user_models
from django.shortcuts import render, redirect
from user.decorators import getUser


@getUser
def check_user(request, obj):
    return request.user == obj.user


@getUser
def QuestionListView(request):
    return render(request, 'post/postlist.html')


@getUser
def QuestionDetailView(request, pk):
    question = get_object_or_404(post_models.Question, id=pk)
    context = {
        'pk': pk,
        'title': question.title,
        'username': request.user.username if request.user.is_authenticated else "",
    }
    return render(request, 'post/postdetail.html', context=context)


@getUser
@login_required
def AskQuestion(request):
    context = {}
    return render(request, 'post/createpost.html', context=context)


@getUser
@login_required
def Draftdetail(request, pk):
    question = get_object_or_404(post_models.Question, id=pk)
    if not check_user(request, question):
        return redirect('post:draflist')
    context = {
        'pk': pk,
        'user': request.user,
    }
    return render(request, 'post/draftdetail.html', context=context)


@getUser
@login_required
def Draflist(request):
    context = {}
    return render(request, 'post/draftlist.html', context=context)


@getUser
@login_required
def CreateAnswer(request, pk):
    question = get_object_or_404(post_models.Question, id=pk)
    context = {
        'pk': pk,
        'title': question.title,
    }
    return render(request, 'post/createanswer.html', context=context)


@getUser
@login_required
def EditQuestion(request, pk):
    question = get_object_or_404(post_models.Question, id=pk)
    if not check_user(request, question):
        return redirect('post:postlist')
    context = {
        'pk': pk,
        'title': question.title,
        'question': True,
        'draft': False,
        'answer': False,
    }
    return render(request, 'post/postupdate.html', context=context)


@getUser
@login_required
def EditDraft(request, pk):
    question = get_object_or_404(post_models.Question, id=pk)
    if not check_user(request, question) or question.published_date:
        return redirect('post:postlist')
    context = {
        'pk': pk,
        'title': question.title,
        'question': False,
        'draft': True,
        'answer': False,
    }
    return render(request, 'post/draftedit.html', context=context)


@getUser
@login_required
def EditAnswer(request, pk_q, pk_a):
    answer = get_object_or_404(post_models.Answer, id=pk_a)
    if not check_user(request, answer):
        return redirect('post:postlist')
    context = {
        'pk_q': pk_q,
        'pk_a': pk_a,
        'title': "Answer Edit",
        'title_q': get_object_or_404(post_models.Question, id=pk_q).title,
        'question': False,
        'draft': False,
        'answer': True,
    }
    return render(request, 'post/answeredit.html', context=context)


@getUser
@login_required
def pulished_darf(request, pk):
    """
    publish question
    """
    question = get_object_or_404(post_models.Question, id=pk)
    if request.user == question.user:
        question.publish()
        return redirect('post:draflist')
    return redirect('post:postdetail')
