"""rest freamwork import"""
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework import (
    viewsets,
    generics,
    authentication,
    permissions,
    filters,
    status,
    pagination,
)
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

"""models import"""
from django.conf import settings
from post import models as post_models
from user import models as user_models

"""serializer import"""
from api import serializers

"""custom permission import"""
from api import api_permissions

"""custom filet import"""


class CreateUserView(generics.CreateAPIView):
    """create user"""
    serializer_class = serializers.UserSerializer



class CreateTokenView(ObtainAuthToken):
    """create token for login"""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManagerUserView(generics.RetrieveUpdateAPIView):
    """manage user"""
    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,api_permissions.UpdateOwnStatus,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """retrieve and return authenticated user"""
        return self.request.user

    def patch(self, request, *args, **kwargs):
        """update user"""
        new_dict = dict(**self.request.data)
        user = self.get_object()
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class AnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = post_models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, api_permissions.UpdateOwnStatus,)
    pagination_class = pagination.PageNumberPagination

    def perform_create(self, serializer):
        temp_path = self.request.get_full_path().split('/')
        serializer.save(user=self.request.user, question=post_models.Question.objects.get(id=temp_path[3]))

    def get_queryset(self, pk=None, **kwargs):
        if not pk:
            temp_path = self.request.get_full_path().split('/')
            # return self.queryset.filter(question__id__in=temp_path[3])
            return self.queryset.filter(question=post_models.Question.objects.get(id= temp_path[3]))
        return self.queryset

class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = post_models.Question.objects.filter(published_date__isnull=False)
    serializer_class = serializers.QuestionSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, api_permissions.UpdateOwnStatus,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)
    pagination_class = pagination.PageNumberPagination
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DarfViewSet(viewsets.ModelViewSet):
    """
    Draf Question publish or edit.
    """
    queryset = post_models.Question.objects.filter(published_date__isnull=True)
    serializer_class = serializers.QuestionSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (
        permissions.IsAuthenticated,
        api_permissions.UpdateOwnStatus,
    )
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self, **kwargs):
        return self.queryset.filter(user=self.request.user)


# @api_view(('GET',))
# def pulished_darf(request, pk):
#     """
#     publish question
#     """
#     print(request.user)
#     question = get_object_or_404(post_models.Question, id=pk)
#     if request.user == question.user:
#         question.publish()
#         return Response(status=status.HTTP_200_OK)
#     return Response(status=status.HTTP_401_UNAUTHORIZED)
