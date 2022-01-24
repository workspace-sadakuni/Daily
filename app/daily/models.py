from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)
from django.db import models
from django.utils import timezone


class Users(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    picture = models.FileField(blank=True, null=True, upload_to='profile/')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'


class UserSessions(models.Model):
    user_id = models.ForeignKey(Users, models.CASCADE, db_column='user_id')
    email = models.TextField(blank=True, null=True)
    session_key = models.TextField(db_index=True, unique=True)
    login_at = models.DateTimeField(null=True)
    last_used_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'user_sessions'


class UserAccessLogs(models.Model):
    request_at = models.DateTimeField(blank=True, null=True)
    response_at = models.DateTimeField(blank=True, null=True)
    user_id = models.ForeignKey(Users, models.CASCADE, db_column='user_id')
    username = models.TextField(blank=True)
    user_email = models.TextField(blank=True)
    request_method = models.TextField(blank=True)
    request_url = models.TextField(blank=True)
    referer = models.TextField(blank=True)
    source_ip = models.TextField(blank=True)
    user_agent = models.TextField(blank=True)
    session_id = models.IntegerField(blank=True)
    session_key = models.TextField(blank=True)
    response_time = models.IntegerField(blank=True)
    status_code = models.TextField(blank=True)

    class Meta:
        db_table = 'user_access_logs'


class PostFoods(models.Model):
    user_id = models.ForeignKey(Users, models.CASCADE, db_column='user_id')
    title = models.TextField(blank=True)
    food_name = models.TextField(blank=True)
    content = models.TextField(blank=True)
    image = models.FileField(blank=True, null=True, upload_to='foods/')
    ate_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    last_updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'post_foods'
