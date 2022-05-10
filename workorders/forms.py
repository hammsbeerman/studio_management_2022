from django.utils.safestring import mark_safe
from django import forms
from .models import Workorder, WorkorderService, WorkorderInventoryProduct, WorkorderNonInventoryProduct
from customers.models import Customer, Contact
from dynamic_forms import DynamicField, DynamicFormMixin

##Attempt at HTMX Dropdown
"""class WorkorderDynamicForm(DynamicFormMixin, forms.Form):

    def contact_choices(form):
        customer = form['customer'].value()
        return Contact.objects.filter(customer=customer)

    def initial_contact(form):
        customer = form['customer'].value()
        return Contact.objects.filter(customer=customer).first()

    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        initial=Customer.objects.first()
    )

    contact = DynamicField(
        forms.ModelChoiceField,
        queryset=contact_choices,
        initial=initial_contact
    )
"""
class WorkorderForm(DynamicFormMixin, forms.ModelForm):
    required_css_class = 'required-field'
    #Attempt at Dynamic Form
    """def contact_choices(form):
        customer = form['customer'].value()
        return Contact.objects.filter(customer=customer)

    def initial_contact(form):
        customer = form['customer'].value()
        return Contact.objects.filter(customer=customer).first()

    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        initial=Customer.objects.first()
    )
    
    contact = DynamicField(
        forms.ModelChoiceField,
        queryset=contact_choices,
        initial=initial_contact
    )"""

    #########################################
    #name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Customer name"}))
    #customer = forms.CharField(widget=forms.TextInput(), label=mark_safe('Customer - (<a href="/customers/create/" target="_blank">Add Customer</a>)'))
    #active = forms.BooleanField(widget=forms.CheckboxInput(attrs={"default": "True"}))
    class Meta:
        model = Workorder
        fields = ['contact', 'workorder', 'description', 'deadline', 'budget', 'quoted_price']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
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
        #self.fields['directions'].widget.attrs.update({'rows': '4'})
        self.fields['contact'].label = ''

class WorkorderServiceForm(forms.ModelForm):
    class Meta:
        model = WorkorderService
        fields = ['item', 'description', 'billable_time', 'default_rate', 'custom_rate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
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
        fields = ['item', 'description', 'qty', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
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
        fields = ['item', 'description', 'qty', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
            new_data = {
                "placeholder": f'{str(field)}',
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )