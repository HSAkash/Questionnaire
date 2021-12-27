from django.urls import path
from post import views

app_name = 'post'


urlpatterns = [
    path('', views.QuestionListView, name='postlist'),
    path('question/<int:pk>/answer/', views.CreateAnswer, name='createanswer'),
    path('question/<int:pk_q>/answer/<int:pk_a>/edit/',
         views.EditAnswer, name='answeredit'),
    path('question/<int:pk>/edit/', views.EditQuestion, name='editpost'),
    path('question/<int:pk>/', views.QuestionDetailView, name='postdetail'),
    path('question/new/', views.AskQuestion, name='postcreate'),
    path('draft/<int:pk>/edit/', views.EditDraft, name='draftedit'),
    path('draft/<int:pk>/publish/', views.pulished_darf, name='draf_publish'),
    path('draft/<int:pk>/', views.Draftdetail, name='draftdetail'),
    path('draft/', views.Draflist, name='draflist'),
]
