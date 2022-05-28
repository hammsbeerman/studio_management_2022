from django.db import models
from django.urls import reverse
from vendors.models import Vendor#, VendorPartNumber



# Create your models here.

"""
Inventory
    - master part numbers
    - Price
    - Measurement
    - Date Added
    - Inventory Qty
    - Inventory Correction
    - Inventory Correction Date
    - Active
    - Vendor
        - Vendor Part Number
        - Vendor last price
        - Vendor last purchase date


Purchase Order
    - Vendor
    - Internal Part Number
    - Vender Part Number
    - Purchase Date
    - Qty
    - Price

"""
class ProductCategory(models.Model):
    SERVICE = 'S'
    INVENTORY = 'I'
    NONINVENTORY = 'N'
    TYPE_CHOICES = [
        (SERVICE, 'Service'),
        (INVENTORY, 'Inventory'),
        (NONINVENTORY, 'Non-Inventory')
    ]
    type = models.CharField('Type', max_length=10, choices=TYPE_CHOICES, blank=False, null=False) #Service,Inventory,NonInventory (Trouple options)
    name = models.CharField('Name', max_length=100, blank=False, null=False) #Category Name
    parent = models.CharField('Parent', max_length=100, blank=True, null=True) #Parent Category ID

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("inventory:category-list", kwargs={"parent": self.id})

class Manufacturer(models.Model):
    name = models.CharField('name', blank=False, null=False, max_length=200)

    def __str__(self):
        return self.name

class Measurement(models.Model):
    name = models.CharField('Name', max_length=100, blank=False, null=False, unique=True)
    abbreviation = models.CharField('Abbreviation', max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

class MasterPartNumber(models.Model):
    internal_part_number = models.CharField('Master Part Number', blank=False, null=False, max_length=200)
    name = models.CharField('Name', max_length=100, blank=True, null=True)
    category = models.ForeignKey(ProductCategory, blank=True, null=True, on_delete=models.SET_NULL)
    #manufacturer = models.CharField('Manufacturer', max_length=100, blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.CharField('Description', max_length=100, blank=True, null=True)
    primary_vendor = models.ForeignKey(Vendor, blank=True, null=True, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement, blank=True, null=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now = True, blank=False, null=False)
    date_updated = models.DateTimeField(auto_now = True, blank=False, null=False)
    active= models.BooleanField(default=True)

    def __str__(self):
        return self.internal_part_number

    def get_absolute_url(self):
        return reverse("inventory:mpn-detail", kwargs={"id": self.id})

    def get_edit_url(self): #reference these, that way changes are only made one place
        return reverse("inventory:mpn-update", kwargs={"id": self.id})



class Inventory(models.Model):
    name = models.CharField('Name', max_length=100, blank=True, null=True, unique=True)
    description = models.CharField('Description', max_length=100, blank=True, null=True)
    category = models.ForeignKey(ProductCategory, blank=True, null=True, on_delete=models.SET_NULL)
    #master_part_number = models.CharField('Master Part Number', max_length=100, blank=True, null=True)
    master_part_number = models.ForeignKey(MasterPartNumber, blank=True, null=True, on_delete=models.SET_NULL)
    price = models.CharField('Price', max_length=100, blank=True, null=True)
    measurement = models.ForeignKey(Measurement, blank=True, null=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now = True, blank=False, null=False)
    inventory_qty = models.CharField('Inventory Qty', max_length=100, blank=True, null=True) #for corrected inventory count
    inventory_correction = models.CharField('Inventory Correction', max_length=100, blank=True, null=True) #amount +/- correction
    inventory_correction_date = models.DateTimeField(auto_now = True, blank=False, null=False) #date of phusical inventory
    active= models.BooleanField(default=True)

    def __str__(self):
        return self.name

"""
class InternalPart(models.Model):
    master_part_number = models.ForeignKey(MasterPartNumber, blank=True, null=True, on_delete=models.SET_NULL)
    vendor_part_number = models.ForeignKey(VendorPartNumber, blank=True, null=True, on_delete=models.SET_NULL)
"""


class NonInventory(models.Model):
    name = models.CharField('Name', max_length=100, blank=False, null=False)
    description = models.CharField('Description', max_length=100, blank=True, null=True)
    category = models.ForeignKey(ProductCategory, blank=True, null=True, on_delete=models.SET_NULL)
    master_part_number = models.CharField('Master Part Number', max_length=100, blank=True, null=True)
    description = models.CharField('Description', max_length=100, blank=True, null=True)
    price = models.CharField('Price', max_length=100, blank=True, null=True)
    measurement = models.ForeignKey(Measurement, blank=True, null=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now = True, blank=False, null=False)
    active= models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField('Name', max_length=100, blank=False, null=False, unique=True)
    category = models.ForeignKey(ProductCategory, blank=True, null=True, on_delete=models.SET_NULL)
    master_part_number = models.CharField('Master Part Number', max_length=100, blank=True, null=True)
    description = models.CharField('Description', max_length=100, blank=True, null=True)
    price = models.CharField('Price', max_length=100, blank=True, null=True)
    measurement = models.ForeignKey(Measurement, blank=True, null=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now = True, blank=False, null=False)
    active= models.BooleanField(default=True)

    def __str__(self):
        return self.name