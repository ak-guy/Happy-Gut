from django.contrib import admin
from vendor.models import Vendor

# Register your models here.
class CustomVendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'restaurant_name')
    list_editable = ('is_approved',)

admin.site.register(Vendor, CustomVendorAdmin)