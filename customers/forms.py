from django import forms
from .models import Customer, Contact

class CustomerForm(forms.ModelForm):
    required_css_class = 'required-field'
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Customer name"}))
    #active = forms.BooleanField(widget=forms.CheckboxInput(attrs={"default": "True"}))
    class Meta:
        model = Customer
        fields = ['name',  'address1',  'address2', 'city', 'state', 'zipcode', 'phone1', 'phone2', 'email', 'website', 'active']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
            new_data = {
                "placeholder": f'Customer {str(field)}',
                "class": 'form-control',
                #"hx-post": "",
                #"hx-trigger": "keyup changed delay:500ms",
                #"hx-target": "#recipe-container",
                #"hx-swap": "outerHTML"
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )
        #self.fields['description'].widget.attrs.update({'rows': '2'})
        #self.fields['directions'].widget.attrs.update({'rows': '4'})

       

class CustomerContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['fname', 'lname', 'phone1', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
            new_data = {
                "placeholder": f'Contact {str(field)}',
                "class": 'form-control',
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )