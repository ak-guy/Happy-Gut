from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

def detectUser(user):
    '''
    This function will help us user role and after logging in it will 
    redirect user to their respective dashboard
    '''
    redirecturl = 'login'
    if user.role == 1:
        redirecturl = 'venddashboard'
    elif user.role == 2:
        redirecturl = 'custdashboard'
    elif user.role == None and user.is_superadmin:
        redirecturl = '/admin'
    
    return redirecturl

def send_verification_mail(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Please activate you account'
    message = render_to_string('accounts/emails/account_verification_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, to=[to_email])
    mail.send()
    print("mail sent successfully to {}".format(to_email))