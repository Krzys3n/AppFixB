from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class MyUserManager(BaseUserManager):

    def create_user(self,login , email, password=None):
        if not email:
            raise ValueError('Email must be provided')
        if not login:
            raise ValueError('Login must be provided')

        user = self.model(login=login, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,login, email, password, **kwargs):
        user = self.create_user(login,email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def user_login(self, request, user):
        if hasattr(user, 'last_activity'):
            user.last_activity = timezone.now()
            user.save()
        user_logged_in.send(sender=user.__class__, request=request, user=user)

    def user_logout(self, request, user):
        if hasattr(user, 'last_activity'):
            user.last_activity = timezone.now()
            user.save()
        user_logged_out.send(sender=user.__class__, request=request, user=user)