# from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User

from django.contrib import messages


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
            pass
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registeruser.html', context)