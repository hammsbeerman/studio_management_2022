from django.urls import reverse
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import ProductCategory, MasterPartNumber, Manufacturer, Service, Inventory, Measurement
from .forms import CategoryForm, MPNForm, ManufacturerForm, ServiceForm, InventoryForm, MeasurementForm

# Create your views here.

#@login_required
def category_list_view(request, parent=None):
    #qs = Customer.objects.filter(user=request.user)
    if parent is None:
        print("None")
        #qs = ProductCategory.objects.all().order_by('parent')
        qs = ProductCategory.objects.filter(parent=None).order_by('parent')
        context = {
         "object_list": qs
        }
        return render(request, "inventory/category-list.html", context)
    else: 
        qs = ProductCategory.objects.filter(parent=parent).order_by('name')
        print(qs)
        context = {
         "object_list": qs
        }
        return render(request, "inventory/category-list.html", context)

#Master Part Number Views

#@login_required
def mpn_list_view(request):
    #qs = Customer.objects.filter(user=request.user)
    qs = MasterPartNumber.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "inventory/mpn-list.html", context)

#@login_required
def mpn_create_view(request):
    form = MPNForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        if request.htmx:
            headers = {
                "HX-Redirect": obj.get_absolute_url()
            }
            return HttpResponse("Created", headers=headers)
        return redirect(obj.get_absolute_url())
    return render(request, "inventory/add-update-mpn.html", context)

#@login_required
def mpn_detail_view(request, id=None):
    hx_url = reverse("inventory:hx-mpn-detail", kwargs={"id": id})
    context = {
        "hx_url": hx_url
    }
    return render(request, "inventory/mpn-detail.html", context)

#@login_required
def mpn_detail_hx_view(request, id=None):
    if not request.htmx:
        #print("Here 1")
        raise Http404
    try:
        obj = MasterPartNumber.objects.get(id=id)
    except:
        obj = None
    if obj is  None:
        return HttpResponse("Not found.")
    context = {
        "object": obj
    }
    return render(request, "inventory/partials/mpn-detail.html", context) 

#@login_required
def mpn_update_view(request, id=None):
    obj = get_object_or_404(MasterPartNumber, id=id,)
    form = MPNForm(request.POST or None, instance=obj) #instance=obj fills the form with data
    titles = ('true')
    #new_vendor_url = reverse("customers:hx-contact-create", kwargs={"parent_id": obj.id})
    #CustomerContactFormset = modelformset_factory(Contact, form=CustomerContactForm, extra=0)
    #qs = obj.contact_set.all()
    context = {
        "form": form,
        #"formset": formset,
        "object": obj,
        #"new_contact_url": new_contact_url
        "titles": titles,
    }
    #print(form)
    if all([form.is_valid()]):
    #if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        context['message'] = 'Data saved.'
    if request.htmx:
        return render(request, "inventory/partials/forms.html", context)
    return render(request, "inventory/add-update-mpn.html", context)






"""
Get category list with ID
Id would be parent of next subset
get subset where id=parentid
list out all categories with that id
link to add customer to parent id
"""

#@login_required
def manufacturer_create_view(request):
    context = {}
    if request.method == "POST":
        name = request.POST.get("name")
        Manufacturer.objects.create(name=name)
        context['name'] = name
        #return render(request, "inventory/manufacturer-list.html", context=context)
    return render(request, "inventory/add-manufacturer.html", context=context)

#@login_required
def service_create_view(request):
    form = ServiceForm(request.POST or None)
    service_type = ProductCategory.objects.filter(type='S')
    print(service_type)
    context = {
        'form': form,
        'service_type': service_type
    }
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            context['saved'] = "Service was added"
            return render(request, "inventory/service-list.html", context)
    return render(request, "inventory/add-service.html", context)

#@login_required
def service_list_view(request):
    qs = Service.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "inventory/service-list.html", context)

#@login_required
def inventory_create_view(request):
    form = InventoryForm(request.POST or None)
    new_mpn_url = reverse("inventory:add-mpn")
    #new_mpn_url = reverse("inventory:create-mpn")
    inventory_type = ProductCategory.objects.filter(type='I')
    context = {
        'form': form,
        'inventory_type': inventory_type,
        'new_mpn_url': new_mpn_url
    }
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()
            context['saved'] = "Service was added"
            return render(request, "inventory/inventory-list.html", context)
    #if request.htmx:
        #return render(request, "inventory/partials/forms.html", context)
    return render(request, "inventory/add-inventory.html", context)

#@login_required
def inventory_list_view(request):
    qs = Inventory.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "inventory/inventory-list.html", context)

def add_category_view(request):
    form = CategoryForm(request.POST or None)
    obj = ProductCategory.objects.all()
    context = {
        "form": form,
        "object": obj,
    }
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            qs = ProductCategory.objects.filter(parent=None).order_by('parent')
            saved = "Service was added"
            context = {
                "object_list": qs,
                "saved": saved,
                "object": obj,
            }
            return render(request, "inventory/category-list.html", context)
    return render(request, "inventory/add-category.html", context)

def get_parent_view(request):
    form = CategoryForm(request.POST or None)
    cattype = request.GET.get("type")
    print(cattype)
    qs = ProductCategory.objects.filter(type=cattype)
    print(qs)
    #parent = ProductCategory.objects.all.filter(type=cattype)
    context = {
        "form": form,
        "parent": qs,
    }
    return render(request, "inventory/partials/getparent.html", context)

def add_measurement_view(request):
    form = MeasurementForm(request.POST or None)
    context = {
        "form": form,
    }
    if request.method == "POST":
        if form.is_valid():
            form.save()
            saved = "Measurement was saved"
            context = {
                "saved": saved,
                "form": form,
            }
    return render(request, "inventory/add-measurement.html", context)

def mpn_autosuggest(request):
    #print(request.GET)
    query = request.GET.get('term')
    qs = MasterPartNumber.objects.filter(internal_part_number__icontains=query)
    mylist = []
    mylist   += [x.internal_part_number for x in qs]
    return JsonResponse(mylist,safe=False)

def manufacturer_autosuggest(request):
    #print(request.GET)
    query = request.GET.get('term')
    qs = Manufacturer.objects.filter(name__icontains=query)
    print(qs)
    mylist = []
    mylist   += [x.name for x in qs]
    return JsonResponse(mylist,safe=False)

def measurement_autosuggest(request):
    #print(request.GET)
    query = request.GET.get('term')
    qs = Measurement.objects.filter(name__icontains=query)
    print(qs)
    mylist = []
    mylist   += [x.name for x in qs]
    return JsonResponse(mylist,safe=False)

def add_mpn(request):
    form = MPNForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        if request.htmx:
            headers = {
                "HX-Redirect": obj.get_absolute_url()
            }
            return HttpResponse("Created", headers=headers)
        return redirect(obj.get_absolute_url())
    return render(request, "inventory/partials/add-mpn.html", context)