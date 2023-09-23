from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=50)
    restaurant_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.restaurant_name
    
    def save(self, *args, **kwargs):
        '''
        will use this when we click save in admin tab for vendor 
        '''
        if self.pk:
            vendor = Vendor.objects.get(pk=self.pk)
            if vendor.is_approved != self.is_approved:
                print('processing admin approval')
                if self.is_approved:
                    mail_subject = 'Congrats! Your restaurant has been approved'
                    mail_template = 'accounts/emails/admin_approval_email.html'
                    context = {
                        'user': self.user,
                        'is_approved': self.is_approved,
                    }
                    send_notification(mail_subject, mail_template, context)
                else:
                    mail_subject = 'We are sorry to inform, your restaurant has not been approved'
                    mail_template = 'accounts/emails/admin_approval_email.html'
                    context = {
                        'user': self.user,
                        'is_approved': self.is_approved,
                    }
                    send_notification(mail_subject, mail_template, context)
                print("is vendor approved >> {self.is_approved}")
        return super(Vendor, self).save(*args, **kwargs)