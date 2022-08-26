from django.utils.safestring import mark_safe
from django import forms
from .models import Workorder, WorkorderService, WorkorderInventoryProduct, WorkorderNonInventoryProduct, WorkorderInvoice
from customers.models import Customer, Contact
from dynamic_forms import DynamicField, DynamicFormMixin

class WorkorderForm(DynamicFormMixin, forms.ModelForm):
    required_css_class = 'required-field'
    description = forms.CharField(widget=forms.Textarea())
    class Meta:
        model = Workorder
        fields = ['contact', 'workorder', 'description', 'deadline', 'budget', 'quoted_price']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            #print(field)
            new_data = {
                "placeholder": f'{str(field)}',
                "class": 'form-control',
                #"hx-post": "",
                #"hx-trigger": "keyup changed delay:500ms",
                #"hx-target": "#recipe-container",
                #"hx-swap": "outerHTML"
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        self.fields['description'].widget.attrs.update({'rows': '2'})
        self.fields['contact'].label = ''

class WorkorderServiceForm(forms.ModelForm):
    class Meta:
        model = WorkorderService
        fields = ['item', 'description', 'billable_time', 'default_rate', 'custom_rate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            #print(field)
            new_data = {
                "placeholder": f'{str(field)}',
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )

class WorkorderInventoryForm(forms.ModelForm):
    class Meta:
        model = WorkorderInventoryProduct
        fields = ['item', 'description', 'qty', 'price', 'measurement', 'custom_measurement', 'custom_rate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            #print(field)
            new_data = {
                "placeholder": f'{str(field)}',
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )

class WorkorderNonInventoryForm(forms.ModelForm):
    class Meta:
        model = WorkorderNonInventoryProduct
        fields = ['item', 'description', 'qty', 'price', 'measurement', 'custom_measurement', 'custom_rate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            #print(field)
            new_data = {
                "placeholder": f'{str(field)}',
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )

class WorkorderInvoiceForm(forms.ModelForm):
    class Meta:
        model = WorkorderInvoice
        fields = ['description', 'invoice_image']