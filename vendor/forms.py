from django import forms
from .models import Vendor
from accounts.validators import allow_only_images_validator

class VendorForm(forms.ModelForm):
    restaurant_license = forms.FileField(validators=[allow_only_images_validator])

    class Meta:
        model = Vendor
        fields = ['restaurant_name', 'restaurant_license']