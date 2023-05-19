from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)


class UserManager(BaseUserManager):
    """Custom user manager with email"""
    def create_user(self, email, username=None, password=None,  **extra_fields):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have an username")
        user = self.model(email=self.normalize_email(email), username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password, username='admin1'):
        superuser = self.model(email=self.normalize_email(email), username=username, password=password)
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save(using=self._db)

        return superuser

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model with email"""

    email=models.EmailField(max_length=255, unique=True)
    username=models.CharField(max_length=255, unique=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD= 'email'

