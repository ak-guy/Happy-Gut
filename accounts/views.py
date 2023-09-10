# from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserForm
from vendor.forms import VendorForm
from .models import User, UserProfile

from django.contrib import messages, auth


def registerUser(request):
    if request.method == 'POST':
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
    if request.method == 'POST':
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.RESTAURANT
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "Your Account has been created Successfully!!")
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

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('dashboard')
        else:
            messages.error(request, "Please enter correct email and password")
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    pass

def dashboard(request):
    return render(request, 'accounts/dashboard.html')