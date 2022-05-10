from django.db import models
from django.urls import reverse
from vendors.models import Vendor
from inventory.models import MasterPartNumber

# Create your models here.

class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, blank=True, null=True, on_delete=models.CASCADE)
    invoice_date = models.DateTimeField(auto_now = True, blank=False, null=False)
    vendor_order_number = models.CharField('Vendor Order Number', max_length=100, blank=True, null=True)
    vendor_part_number = models.CharField('Vendor Part Number', max_length=100, blank=True, null=True)
    internal_part_number = models.ForeignKey(MasterPartNumber, blank=True, null=True, on_delete=models.CASCADE)
    description = models.CharField('Description', max_length=100, blank=True, null=True)
    qty = models.CharField('Qty', max_length=100, blank=True, null=True)
    item_price = models.CharField('Price', max_length=100, blank=True, null=True)
    pkg_qty = models.CharField('Package Qty', max_length=100, blank=True, null=True)
    shipping_cost = models.CharField('Shipping Cost', max_length=100, blank=True, null=True)
    tax = models.CharField('Tax', max_length=100, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now = True, blank=False, null=False)
    date_received = models.DateTimeField(auto_now = True, blank=False, null=False)

    #def __str__(self):
     #   return f'{self.vendor} {self.date_ordered}'

    def __str__(self):
        return self.vendor

    def get_absolute_url(self):
        return reverse("purchase_orders:po-detail", kwargs={"id": self.id})
    
    #def get_hx_url(self):
    #    return reverse("inventory:hx-po-detail", kwargs={"id": self.id})

