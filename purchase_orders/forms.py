from django import forms
from inventory.models import MasterPartNumber
from .models import PurchaseOrder

class POForm(forms.ModelForm):
    required_css_class = 'required-field'
    #name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Customer name"}))
    #active = forms.BooleanField(widget=forms.CheckboxInput(attrs={"default": "True"}))
    class Meta:
        model = PurchaseOrder
        fields = ['vendor', 'vendor_order_number', 'vendor_part_number', 'internal_part_number', 'description', 'qty', 'item_price', 'pkg_qty', 'shipping_cost', 'tax']
    
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
        #self.fields['description'].widget.attrs.update({'rows': '2'})
        #self.fields['directions'].widget.attrs.update({'rows': '4'})