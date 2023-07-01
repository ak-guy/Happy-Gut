from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import *

@receiver(post_save, sender=User)
def post_save_create_profile_receuver(sender, instance, created, **kwargs):
    '''as soon as we get created=True or User is created, we will then create userprofile
    '''
    print(created)
    if created:
        try:
            UserProfile.objects.create(user=instance)
            print("UserProfile created successfully")
        except Exception as e:
            print("Exception >>> ", e)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print("userprofile updated")
        except Exception as e:
            print("Exception >>> ", e)
            UserProfile.objects.create(user=instance)
            print("UserProfile created successfully")