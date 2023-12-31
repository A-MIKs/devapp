from .models import *
from django.db.models.signals import post_save, post_delete
from django.core.mail import send_mail
from django.conf import settings

def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(user=user, username=user.username,
                                email=user.email, name=user.first_name)
        subject = "DevSearch"
        message = "We are glad you are here!"
        send_mail(subject, message,
                   settings.EMAIL_HOST_USER, [profile.email], fail_silently=False)

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if not created:
        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleteUser(sender, instance, **kwargs):
    user= instance.user
    user.delete()


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
