from django.shortcuts import render, get_object_or_404, redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm
from django.contrib import messages

from accounts.models import UserProfile
from .models import Vendor
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor

from menu.models import * 

from vendor.utils import get_vendor

# Create your views here.


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings has been updated')
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
            messages.error(request, 'Settings has not been updated')
    else:
        profile_form = UserProfileForm(instance=profile) # passing instance will help form load the existing data
        vendor_form = VendorForm(instance=vendor) # passing instance will help form load the existing data

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, "vendors/vprofile.html", context=context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    context = {
        'categories': categories,
    }
    return render(request, 'vendors/menu-builder.html', context=context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    food_items = FoodItem.objects.filter(vendor=vendor, category=category)
    context = {
        'food_items': food_items,
        'category': category
    }
    return render(request, 'vendors/fooditems_by_category.html', context=context)