from django.contrib import admin

# Register your models here.
from .models import Workorder, WorkorderService, WorkorderInventoryProduct, WorkorderNonInventoryProduct, WorkorderInvoice


class WorkorderServiceInline(admin.StackedInline):
    model = WorkorderService
    extra = 1

class WorkorderInventoryInline(admin.StackedInline):
    model = WorkorderInventoryProduct
    extra = 1

class WorkorderNonInventoryInline(admin.StackedInline):
    model = WorkorderNonInventoryProduct
    extra = 1

class WorkorderInvoiceInline(admin.StackedInline):
    model = WorkorderInvoice



class WorkorderAdmin(admin.ModelAdmin):
    inlines = [WorkorderServiceInline, WorkorderInventoryInline, WorkorderNonInventoryInline, WorkorderInvoiceInline]
    

admin.site.register(Workorder, WorkorderAdmin)