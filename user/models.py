from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django_resized import ResizedImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from django.core.files.base import ContentFile


def upload_location(instance, filename, **kwargs):
    """Upload location for profile image"""
    return f"accounts/{instance.username}/{filename}"

def upload_logo_location(instance, filename, **kwargs):
    """Upload location for profile image"""
    return f"accounts/{instance.user.username}/{filename}"



class UserProfileManager(BaseUserManager):
    """Manage for user profile"""

    def create_user(self, email, username, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError('User must have a password')
        if not username:
            raise ValueError('User must have a username')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        """Create and save a new superuser with given details"""
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError('User must have a password')
        if not username:
            raise ValueError('User must have a username')
        email = self.normalize_email(email)
        user = self.create_user(email = email,
            username = username,
            password = password
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50, unique=True)
    image = models.ImageField(
        upload_to=upload_location,
        default='DefaultImages/user.jpg',
        null=False, blank=True
    )

    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserProfileManager()

    def __str__(self):
        """Retrieve full name of user"""
        return self.username

class UserLogo(models.Model):
    """Database model for user Logo"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='logouser')
    icon = ResizedImageField(size=[200, 200], quality=100, upload_to=upload_logo_location, blank=True, null=True)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user logo before save"""
    try:
        picture_copy = ContentFile(instance.image.read())
        logo = UserLogo.objects.get_or_create(user=instance)[0]
        logo.icon.save('logo.jpg', picture_copy)
    except:
        pass

