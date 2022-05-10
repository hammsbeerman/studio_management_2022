from django.contrib import admin

# Register your models here.
from .models import PurchaseOrder

admin.site.register(PurchaseOrder)