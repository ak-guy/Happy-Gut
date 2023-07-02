# from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User

def registerUser(request):
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
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
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registeruser.html', context)