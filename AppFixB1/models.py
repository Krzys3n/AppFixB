from enum import Enum

from django.db import models

from django.db import models
from django.contrib.auth.models import BaseUserManager

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from .manager import MyUserManager


class User(AbstractBaseUser):
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    login = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    surname = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('User', 'User')], default='User')
    upvotes = models.IntegerField(default=0)
    date_registration = models.DateTimeField(auto_now_add=True)
    github_profile = models.CharField(max_length=255, blank=True, null=True)
    linkedin_profile = models.CharField(max_length=255, blank=True, null=True)
    twitter_profile = models.CharField(max_length=255, blank=True, null=True)
    discord_profile = models.CharField(max_length=255, blank=True, null=True)


    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'password']

    objects = MyUserManager()  # new

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RoleCompany(Enum):
    BOSS = 'boss'
    PROGRAMMER = 'programmer'
    TESTER = 'tester'


class UserCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role_company = models.CharField(max_length=255, choices=[(role.value, role.name) for role in RoleCompany])

    def __str__(self):
        return f"{self.user.username}'s Company"

    class Meta:
        verbose_name_plural = 'UserCompanies'


class AccessChoices(Enum):
    PUBLIC = 'public'
    PRIVATE = 'private'


class App (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255)
    price = models.FloatField(blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    access = models.CharField(max_length=255, choices=[(choice.value, choice.value) for choice in AccessChoices],
                              default=AccessChoices.PUBLIC.value)
    rating = models.DecimalField(max_digits=5, decimal_places=2,blank=True, null = True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Apps'

class Report(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    content = models.TextField()
    solution = models.TextField(blank=True, null=True)

    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)

    priority = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 11)])

    date_created = models.DateTimeField(auto_now_add=True)
    date_solved = models.DateTimeField(blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Reports'

class AppCompany(models.Model):
    id = models.AutoField(primary_key=True)
    id_app = models.ForeignKey(App, on_delete=models.CASCADE)
    id_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    development_plan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"AppCompany: {self.id}"

    class Meta:
        verbose_name_plural = 'AppCompanies'