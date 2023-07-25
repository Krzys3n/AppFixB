from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    user.update_last_login()
    user.update_online_status(True)


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    try:
        user.update_online_status(False)
    except user.DoesNotExist:
        pass
