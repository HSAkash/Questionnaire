from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

app_name = 'api'

router = DefaultRouter()
# router.register('', views.AnswerViewSet, basename='update-viewset')
# router.register('', views.QuestionViewSet)

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('manage/', views.ManagerUserView.as_view(), name='manage'),
    # path('updateprofile/', include(router.urls)),
    # path('draf/<int:pk>/publish', views.pulished_darf, name='draf-publish'),
]

from rest_framework import renderers




question_list = views.QuestionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
question_detail = views.QuestionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

answer_list = views.AnswerViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
answer_detail = views.AnswerViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

darf_list = views.DarfViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

darf_detail = views.DarfViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns += format_suffix_patterns([
    path('question/', question_list, name='question-list'),
    path('question/<int:pk>/', question_detail, name='question-detail'),
    path('question/<int:question>/answer/', answer_list, name='answer-list'),
    path('question/<int:question>/answer/<int:pk>/', answer_detail, name='answer-detail'),
    path('draf/', darf_list, name='draf-list'),
    path('draf/<int:pk>/', darf_detail, name='draf-detail'),
])

# urlpatterns += path('draf/<int:pk>/publish/', views.pulished_darf, name='draf-publish'),
