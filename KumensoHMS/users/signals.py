import sys
import os
parent_dir = os.path.abspath("..")
sys.path.append(parent_dir)#from Tools.demo.mcast import sender


from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import MyUser,Profile
from patient_management.models import Vitals, CheckIn


@receiver(post_save, sender=MyUser)
def create_profile(instance, sender, created, **kwargs):
    if created:
        print('create_profile')
        Profile.objects.create(user=instance)

@receiver(post_save, sender=MyUser)
def save_profile(instance, sender, **kwargs):
    print('save_profile')
    instance.profile.save()
    print(instance.profile)



