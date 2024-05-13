from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserProfile

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.is_online = True
    print('User logged in!!!')
    profile.save()

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    try:
        profile = user.userprofile
        profile.is_online = False
        print('User logged out!!!')
        profile.save()
    except UserProfile.DoesNotExist:
        pass
