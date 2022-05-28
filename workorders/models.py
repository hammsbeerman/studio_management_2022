from time import time
from django.db import models
from django.conf import settings
from django.urls import reverse
from inventory.utils import number_str_to_float
from inventory.validators import validate_unit_of_measure
from customers.models import Customer, Contact
from inventory.models import NonInventory, Inventory, Service
#import pint

# Create your models here.
class Workorder(models.Model):
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, blank=True, null=True, on_delete=models.SET_NULL)
    #company = models.OneToOneField(Customer, on_delete=models.CASCADE, blank=True, null=True)
    workorder = models.CharField('Workorder', max_length=100, blank=False, null=False, unique=True)
    description = models.CharField('Description', max_length=100, blank=True, null=True)
    deadline = models.DateField('Deadline', blank=True, null=True)
    budget = models.CharField('Budget', max_length=100, blank=True, null=True)
    quoted_price = models.CharField('Quoted Price', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.workorder

    def get_absolute_url(self):
        #return "/pantry/recipes/"
        return reverse("workorders:detail", kwargs={"id": self.workorder})

    def get_edit_url(self): #reference these, that way changes are only made one place
        return reverse("workorders:update", kwargs={"id": self.id})

    def get_contacts_children(self):
        return self.contact_set.all()

    def get_services_children(self):
        return self.workorderservice_set.all()

    def get_inventory_children(self):
        return self.workorderinventoryproduct_set.all()

    def get_noninventory_children(self):
        return self.workordernoninventoryproduct_set.all()

class WorkorderService(models.Model):
    workorder = models.ForeignKey(Workorder, blank=False, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Service, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.CharField('Description', max_length=200, blank=True, null=True)
    billable_time = models.DecimalField('Billable Time', max_digits=10, decimal_places=2, blank=True, null=True)
    default_rate = models.DecimalField('Default Rate', max_digits=10, decimal_places=2, blank=True, null=True)
    custom_rate = models.DecimalField('Custom Rate', max_digits=10, decimal_places=2, blank=True, null=True)

    #def __str__(self):
    #    return self.item.name

    def get_absolute_url(self):
        return self.workorder.get_absolute_url()
    
    def get_hx_edit_url(self):
        kwargs = {
            "parent_id": self.workorder.id,
            "id": self.id
        }
        return reverse("workorders:hx-workorder-service-detail", kwargs=kwargs)
    
    @property
    def line_total_default(self):
        if self.billable_time is None:
            billable = 0
        else:
            billable = float(self.billable_time)
        if self.custom_rate is None:
            self.custom_rate = 0
            if self.default_rate is None:
                print(2)
                self.default_rate = 0
                rate = 0
            else:
                print(3)
                rate = float(self.default_rate)
        if self.custom_rate == 0:
            print(4)
            rate = float(self.default_rate)
        else:
            print(5)
            rate = float(self.custom_rate)
        line = billable * rate
        line = '$' + format(line, ',.2f')
        return line

   # @property
    #def Line_total_default(self):
    #	line = self.default_rate * self.billable_time
	#    return line_total_default

class WorkorderInventoryProduct(models.Model):
    workorder = models.ForeignKey(Workorder, blank=False, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Inventory, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.CharField('Description', max_length=100, blank=True, null=True)
    qty = models.CharField('Qty', max_length=100, blank=True, null=True)
    price = models.CharField('Price', max_length=100, blank=True, null=True)

    #def __str__(self):
    #    return self.item.name

    def get_absolute_url(self):
        return self.workorder.get_absolute_url()
    
    def get_hx_edit_url(self):
        kwargs = {
            "parent_id": self.workorder.id,
            "id": self.id
        }
        return reverse("workorders:hx-workorder-inventory-detail", kwargs=kwargs)

class WorkorderNonInventoryProduct(models.Model):
    workorder = models.ForeignKey(Workorder, blank=False, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(NonInventory, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.CharField('Description', max_length=100, blank=True, null=True)
    qty = models.CharField('Qty', max_length=100, blank=True, null=True)
    price = models.CharField('Price', max_length=100, blank=True, null=True)

    #def __str__(self):
    #    return self.item.name

    def get_absolute_url(self):
        return self.workorder.get_absolute_url()
    
    def get_hx_edit_url(self):
        kwargs = {
            "parent_id": self.workorder.id,
            "id": self.id
        }
        return reverse("workorders:hx-workorder-noninventory-detail", kwargs=kwargs)
