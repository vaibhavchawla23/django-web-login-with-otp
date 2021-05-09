from .models import Patient , Doctor, Code
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver (user_logged_in)
def update_profile(sender, user, request, **kwargs):

    if user_logged_in:
      print ("User ID and Password OK For = " ,user)
      if Code.objects.update_or_create(user=user):
        print ("Fresh OTP Successfully Published For = " ,user)
