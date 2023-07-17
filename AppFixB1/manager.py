from django.contrib.auth.models import BaseUserManager


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
        user.save(using=self._db)
        return user