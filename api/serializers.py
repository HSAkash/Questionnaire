"""Import Serializer"""
from rest_framework import serializers

"""Import necessary"""
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _


"""Import all models"""
from django.conf import settings
from post import models as post_models
from user import models as user_models
from django.contrib.auth import get_user_model





"""User creation methods, Login  and Logout methods"""
class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'password2', 'image')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            },
        }

    def create(self, validated_data):
        password2 = validated_data.pop('password2', None)
        if not validated_data['password'] == password2:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self,instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2', None)
        if not instance.check_password(password) and password:
            raise serializers.ValidationError({'password': 'Incorrect password'})
        if password and password2 and instance.check_password(password) and password == password2:
            raise serializers.ValidationError({'password': 'New password must be different from old password'})
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password2)
            user.save()

        return user

class UploadImageSerializer(serializers.ModelSerializer):
    """Image serializer"""
    class Meta:
        model = user_models.User
        fields = ('id' ,'image',)
        rearead_only_fields = ('id',)

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs






"""Answer Serializer"""
class AnswerSerializer(serializers.ModelSerializer):
    """Answer Serializer"""
    username = serializers.CharField(source='user.username', read_only=True)
    img_url = serializers.SerializerMethodField()
    answer_edit_url = serializers.SerializerMethodField()
    woner = serializers.SerializerMethodField()
    class Meta:
        model = post_models.Answer
        fields = ('id', 'username', 'img_url', 'description', 'answer_edit_url', 'woner')
        read_only_fields = ('id', 'username', 'img_url', 'answer_edit_url', 'woner')

    def get_answer_edit_url(self, obj):
        """Get answer edit url"""
        request = self.context.get('request')
        url = f"/api/question/{obj.question.id}/answer/{obj.id}"
        return request.build_absolute_uri(url)

    def get_img_url(self, obj):
        """Get img url"""
        request = self.context.get('request')
        return request.build_absolute_uri(user_models.UserLogo.objects.get(user=obj.user).icon.url)
        # return user_models.UserLogo.objects.get(user=obj.user).icon.url
    
    def get_woner(self, obj):
        request = self.context.get('request')
        return  request.user == obj.user

"""Question  serializer"""
class QuestionSerializer(serializers.ModelSerializer):
    """Question  serializer"""
    username = serializers.CharField(source='user.username', read_only=True)
    img_url = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    answer_url = serializers.SerializerMethodField()
    total_answer = serializers.SerializerMethodField()
    publish_url = serializers.SerializerMethodField()
    woner = serializers.SerializerMethodField()
    class Meta:
        model = post_models.Question
        fields = ('id', 'username', 'img_url', 'title', 'description',
            'created_at', 'detail_url', 'answer_url', 'total_answer',
            'published_date', 'publish_url','woner',
        )
        read_only_fields = ('id', 'username', 'img_url', 'created_at',
            'answer_url', 'detail_url', 'total_answer', 'published_date',
            'publish_url', 'woner',
        )

    def get_img_url(self, obj):
        """Get img url"""
        request = self.context.get('request')
        return request.build_absolute_uri(user_models.UserLogo.objects.get(user=obj.user).icon.url)
        # return user_models.UserLogo.objects.get(user=obj.user).icon.url

    def get_detail_url(self, obj):
        """Get detail url"""
        request = self.context.get('request')
        url = f"/api/question/{obj.id}"
        return request.build_absolute_uri(url)

    def get_answer_url(self, obj):
        """Get answer url"""
        request = self.context.get('request')
        url = f"/api/question/{obj.id}/answer"
        return request.build_absolute_uri(url)

    def get_total_answer(self, obj):
        """Get total answer"""
        return post_models.Answer.objects.filter(question=obj).count()

    def get_publish_url(self, obj):
        """Get publish url"""
        if obj.published_date is None:
            request = self.context.get('request')
            url = f"/api/question/{obj.id}/publish"
            return request.build_absolute_uri(url)
        return None

    def get_woner(self, obj):
        request = self.context.get('request')
        return  request.user == obj.user
