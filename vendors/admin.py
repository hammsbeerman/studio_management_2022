from django.contrib import admin

# Register your models here.
from .models import Vendor, VendorContact

class VendorContactInline(admin.StackedInline):
    model = VendorContact
    extra = 0
    readonly_fields = ['created', 'updated']

class VendorAdmin(admin.ModelAdmin):
    inlines = [VendorContactInline]
    readonly_fields = ['created', 'updated']


admin.site.register(Vendor, VendorAdmin)