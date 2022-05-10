from django.contrib import admin

# Register your models here.
from .models import Customer, Contact

class CustomerContactInline(admin.StackedInline):
    model = Contact
    extra = 0
    readonly_fields = ['created', 'updated']

class CustomerAdmin(admin.ModelAdmin):
    inlines = [CustomerContactInline]
    readonly_fields = ['created', 'updated']


admin.site.register(Customer, CustomerAdmin)
