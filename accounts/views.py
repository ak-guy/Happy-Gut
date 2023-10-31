# from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile
from accounts.utils import detectUser, send_verification_mail
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor
from django.http import HttpResponse, JsonResponse
import json

def check_role_vendor(user):
    '''
    '''
    if user.role == 1:
        return True
    raise PermissionDenied

def check_role_customer(user):
    '''
    '''
    if user.role == 2:
        return True
    raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        print("already logged in")
        messages.warning(request, "You are already logged in")
        return redirect('dashboard')
    elif request.method == 'POST':
        ''' response for request.POST ->
        <QueryDict: {'csrfmiddlewaretoken': ['Df3xJaNlRYycqRsDJIFLwrDGd8RyqGIRCpdP7uPPOCPrbxr7IVNMjRCiP4nAFEoD'],
        'first_name': ['arp'], 'last_name': ['ku'], 'email': ['arp@gamil.com'], 'username': ['aks'],
        'password': ['123'], 'confirm_password': ['123']}>
        '''
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Your Account has been created Successfully!!")

            # just after user is created, we will send verification mail
            mail_subject = 'Please activate you account'
            mail_template = 'accounts/emails/account_verification_email.html'
            send_verification_mail(request, user, mail_subject, mail_template)
            return redirect('registerUser')
            '''
            another method to do the same thing will be ->

            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            return redirect('registerUser')
            '''
        else:
            ''' example ->
            <ul class="errorlist"><li>email<ul class="errorlist"><li>User with this Email already exists.</li></ul></li></ul>
            '''
            # print(form.errors)
            messages.error(request, "Please Enter valid information")
            pass
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registeruser.html', context)

def registerVendor(request):
    '''
    while registering vendor we will create an user and allocate it Restaurant role
    also we need to make entry in three tables while registering a vendor; User, UserProfile, Vendor
    '''
    if request.user.is_authenticated:
        print("already logged in")
        messages.warning(request, "You are already logged in")
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print(email)
            print(password)
            user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email)
            user.set_password(password)
            user.role = User.RESTAURANT
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "Your Account has been created Successfully!!")

            # just after user is created, we will send verification mail
            mail_subject = 'Please activate you account'
            mail_template = 'accounts/emails/account_verification_email.html'
            send_verification_mail(request, user, mail_subject, mail_template)
            return redirect('registerVendor')
        else:
            print(form.errors)
    else:
        form = UserForm()
        vendor_form = VendorForm()
    context = {
        'form': form,
        'vendor_form': vendor_form,
    }
    return render(request, 'accounts/registerVendor.html', context)

def activate(request, uidb64, token):
    '''
    Activate the user by setting is_active to true
    '''
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user and default_token_generator.check_token(user, token):
        user.is_active =True
        user.save()
        messages.success(request, "Congratulation your account is activated")
        print("valid action link")
        return redirect('myAccount')
    else:
        messages.error(request, "Invalid activation Link")
        return redirect('myAccount')
    

def login(request):
    if request.user.is_authenticated:
        print("already logged in")
        messages.warning(request, "You are already logged in")
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password',None)
        user = auth.authenticate(email=email, password=password)
        print("user")
        print(user)
        if user is not None:
            print("logging in..")
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('myAccount')
        else:
            print(email)
            print(password)
            messages.error(request, "Please enter correct email and password")
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, "You are now logged out")
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirecturl = detectUser(user)
    return redirect(redirecturl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custdashboard(request):
    return render(request, 'accounts/custdashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def venddashboard(request):
    return render(request, 'accounts/venddashboard.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            '''send reset password email
            '''
            mail_subject = 'Please click on this link to reset your password'
            mail_template = 'accounts/emails/reset_password_email.html'
            send_verification_mail(request, user, mail_subject, mail_template)
            messages.success(request, "Password resest link has been sent to your email")
            return redirect('login')
        else:
            messages.error(request, "Account does not exist")
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    '''
    validate the token received
    '''
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user and default_token_generator.check_token(user, token):
        request.session['uid'] = uid # we will use this while updating the password to a particular user
        return redirect('reset_password')
    else:
        messages.error(request, "Invalid activation Link")
        return redirect('myAccount')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Your password has been successfuly updated")
            return redirect('login')
        else:
            messages.error(request, "Passwords does not match")
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')

def test_api(request):
    response_data = {'a': 12, 'codes': 1, 'state': True}
    response_data = json.dumps(response_data)
    return HttpResponse(response_data)