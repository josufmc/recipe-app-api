from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """ Creates and saves a new user """
        if not email:
            raise ValueError('Users must have an email address')
        normalized_email = self.normalize_email(email)  # from BaseUserManager
        user = self.model(email=normalized_email, **extra_fields)
        user.set_password(password)     # from AbstractBaseUser
        user.save(using=self._db)       # Multi DB
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """ Creates and saves a new superuser """
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports using email instead username """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()     # Creates a new user manager

    USERNAME_FIELD = 'email'
