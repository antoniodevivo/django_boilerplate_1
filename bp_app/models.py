from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UsersGroups(models.Model):
    name = models.CharField(max_length=100)
    rank_level = models.IntegerField()

class UserManager(BaseUserManager):

    def create_user(    self, 
                        username, 
                        first_name=None, 
                        last_name=None, 
                        email=None, 
                        password=None):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.group_id = 1
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(   self, 
                            username, 
                            first_name=None, 
                            last_name=None, 
                            email=None, 
                            password=None):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email= email,
            password=password
        )
        user.group_id = 2
        user.is_admin = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    group = models.ForeignKey(UsersGroups,
                                on_delete=models.DO_NOTHING
                                )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def create (self, *args, **kwargs):
        pass
        


