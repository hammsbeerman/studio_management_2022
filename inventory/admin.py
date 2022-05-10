from django.contrib import admin

# Register your models here.
from .models import Inventory, NonInventory, Service, ProductCategory, MasterPartNumber, Manufacturer

admin.site.register(Manufacturer)

admin.site.register(Inventory)

admin.site.register(NonInventory)

admin.site.register(Service)

admin.site.register(ProductCategory)

admin.site.register(MasterPartNumber)

"""
class CustomerContactInline(admin.StackedInline):
    model = Contact
    extra = 0
    readonly_fields = ['created', 'updated']

class CustomerAdmin(admin.ModelAdmin):
    inlines = [CustomerContactInline]
    readonly_fields = ['created', 'updated']


admin.site.register(Customer, CustomerAdmin)
"""