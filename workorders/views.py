from multiprocessing import parent_process
from urllib.request import Request
#from winreg import REG_WHOLE_HIVE_VOLATILE

from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory #modelform for querysets
from django.urls import reverse
from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Workorder, WorkorderService, WorkorderInventoryProduct, WorkorderNonInventoryProduct, WorkorderInvoice
from customers.models import Customer, Contact
from inventory.models import Service, Inventory
from .forms import WorkorderForm, WorkorderServiceForm, WorkorderInventoryForm, WorkorderNonInventoryForm, WorkorderInvoiceForm
#from .forms import WorkorderDynamicForm

# Create your views here.
"""#@login_required
def workorder_create_view(request):
    form = WorkorderForm(request.POST or None)
    context = {
        "form": form,
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
    return render(request, "workorders/add-update.html", context)
"""

#@login_required
def workorder_list_view(request):
    #qs = Customer.objects.filter(user=request.user)
    qs = Workorder.objects.all().order_by('-workorder')
    context = {
        "object_list": qs
    }
    return render(request, "workorders/list.html", context)

#@login_required
def workorder_detail_view(request, id=None):
    hx_url = reverse("workorders:hx-detail", kwargs={"id": id})
    context = {
        "hx_url": hx_url
    }
    return render(request, "workorders/detail.html", context)

#@login_required
def workorder_delete_view(request, id=None):
    #hx_url = reverse("workorders:hx-detail", kwargs={"id": id})
    obj = get_object_or_404(Workorder, id=id,)
    if request.method == "POST":
        obj.delete()
        success_url = reverse('workorders:list')
        return redirect(success_url)
        #return render 
    context = {
        #"hx_url": hx_url
        "object": obj
    }
    return render(request, "workorders/delete.html", context)

#@login_required
def workorder_detail_hx_view(request, id=None):
    if not request.htmx:
        #print("Here 1")
        raise Http404
    try:
        obj = Workorder.objects.get(workorder=id)
    except:
        obj = None
    if obj is  None:
        return HttpResponse("Not found.")
    context = {
        "object": obj
    }
    #print (object.line_total_default)
    return render(request, "workorders/partials/detail.html", context) 

#@login_required
def workorder_update_view(request, id=None):
    obj = get_object_or_404(Workorder, id=id,)
    form = WorkorderForm(request.POST or None, instance=obj) #instance=obj fills the form with data
    titles = ('true')
    new_invoice_url = reverse("workorders:hx-invoice-add", kwargs={"parent_id": obj.id})
    new_service_url = reverse("workorders:hx-service-create", kwargs={"parent_id": obj.id})
    new_inventory_url = reverse("workorders:hx-inventory-create", kwargs={"parent_id": obj.id})
    new_noninventory_url = reverse("workorders:hx-noninventory-create", kwargs={"parent_id": obj.id})
    WorkorderServiceFormset = modelformset_factory(WorkorderService, form=WorkorderServiceForm, extra=1)
    #qs = obj.contact_set.all()
    context = {
        "form": form,
        #"formset": formset,
        "object": obj,
        "titles": titles,
        "new_invoice_url": new_invoice_url,
        "new_service_url": new_service_url,
        "new_inventory_url": new_inventory_url,
        "new_noninventory_url": new_noninventory_url
    }
    #print(form)
    if all([form.is_valid()]):
    #if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        context['message'] = ''
    if request.htmx:
        return render(request, "workorders/partials/forms.html", context)
    return render(request, "workorders/add-update.html", context)

#@login_required
def workorder_service_update_hx_view(request, parent_id= None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Workorder.objects.get(id=parent_id)
    except:
        parent_obj = None
    if parent_obj is  None:
        return HttpResponse("Not found.")
    instance = None
    if id is not None:
        try:
            instance = WorkorderService.objects.get(workorder=parent_obj, id=id)
        except:
            instance = None
    form = WorkorderServiceForm(request.POST or None, instance=instance)
    url = reverse("workorders:hx-service-create", kwargs={"parent_id": parent_obj.id})
    services = Service.objects.all().order_by('-name')
    if instance:
        url = instance.get_hx_edit_url()
    context = {
        "url": url,
        "form": form,
        "object": instance,
        "services": services
    }
    if form.is_valid():
        new_obj=form.save(commit=False)
        if instance is None:
            new_obj.workorder = parent_obj
        cr = request.POST.get("custom_rate")
        print(cr)
        print(new_obj.custom_rate)
        if cr != '':
            cr = float(cr)
            print('$' + format(cr, ',.2f'))
            new_obj.custom_rate = cr
        new_obj.save()
        context['object'] = new_obj
        return render(request, "workorders/partials/service-inline.html", context)
    if id == None:
        return render(request, "workorders/partials/service-add-form.html", context)
    return render(request, "workorders/partials/service-form.html", context)

"""#@login_required
def workorder_inventory_update_hx_view(request, parent_id= None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Workorder.objects.get(id=parent_id)
    except:
        parent_obj = None
    if parent_obj is  None:
        return HttpResponse("Not found.")

    instance = None
    if id is not None:
        #print('1')
        try:
            #print('2')
            instance = WorkorderInventoryProduct.objects.get(workorder=parent_obj, id=id)
        except:
            #print('3')
            instance = None
    form = WorkorderInventoryForm(request.POST or None, instance=instance)
    url = reverse("workorders:hx-inventory-create", kwargs={"parent_id": parent_obj.id})
    if instance:
        url = instance.get_hx_edit_url()
    context = {
        "url": url,
        "form": form,
        "object": instance
    }
    if form.is_valid():
        new_obj=form.save(commit=False)
        if instance is None:
            new_obj.workorder = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "workorders/partials/inventory-inline.html", context) 
    return render(request, "workorders/partials/inventory-form.html", context)
"""

def workorder_inventory_update_hx_view(request, parent_id= None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Workorder.objects.get(id=parent_id)
    except:
        parent_obj = None
    if parent_obj is  None:
        return HttpResponse("Not found.")
    instance = None
    if id is not None:
        try:
            instance = WorkorderInventoryProduct.objects.get(workorder=parent_obj, id=id)
        except:
            instance = None
    form = WorkorderInventoryForm(request.POST or None, instance=instance)
    url = reverse("workorders:hx-inventory-create", kwargs={"parent_id": parent_obj.id})
	#
    inventorys = Inventory.objects.all().order_by('-name')
    if instance:
        url = instance.get_hx_edit_url()
    context = {
        "url": url,
        "form": form,
        "object": instance,
		#
        "inventorys": inventorys
    }
    if form.is_valid():
        new_obj=form.save(commit=False)
        if instance is None:
            new_obj.workorder = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "workorders/partials/inventory-inline.html", context)
    if id == None:
        return render(request, "workorders/partials/inventory-add-form.html", context)
    return render(request, "workorders/partials/inventory-form.html", context)


#@login_required
def workorder_noninventory_update_hx_view(request, parent_id= None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Workorder.objects.get(id=parent_id)
    except:
        parent_obj = None
    if parent_obj is  None:
        return HttpResponse("Not found.")

    instance = None
    if id is not None:
        #print('1')
        try:
            #print('2')
            instance = WorkorderNonInventoryProduct.objects.get(workorder=parent_obj, id=id)
        except:
            #print('3')
            instance = None
    form = WorkorderNonInventoryForm(request.POST or None, instance=instance)
    url = reverse("workorders:hx-noninventory-create", kwargs={"parent_id": parent_obj.id})
    if instance:
        url = instance.get_hx_edit_url()
    context = {
        "url": url,
        "form": form,
        "object": instance
    }
    if form.is_valid():
        new_obj=form.save(commit=False)
        if instance is None:
            new_obj.workorder = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "workorders/partials/noninventory-inline.html", context) 
    return render(request, "workorders/partials/noninventory-form.html", context)

#@login_required
def workorder_invoice_update_hx_view(request, parent_id= None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Workorder.objects.get(id=parent_id)
    except:
        parent_obj = None
    if parent_obj is  None:
        return HttpResponse("Not found.")

    instance = None
    if id is not None:
        #print('1')
        try:
            #print('2')
            instance = WorkorderInvoice.objects.get(workorder=parent_obj, id=id)
        except:
            #print('3')
            instance = None
    form = WorkorderInvoiceForm(request.POST or None, instance=instance)
    url = reverse("workorders:hx-invoice-add", kwargs={"parent_id": parent_obj.id})
    if instance:
        url = instance.get_hx_edit_url()
    context = {
        "url": url,
        "form": form,
        "object": instance
    }
    if form.is_valid():
        new_obj=form.save(commit=False)
        if instance is None:
            new_obj.workorder = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "workorders/partials/invoice-inline.html", context) 
    return render(request, "workorders/partials/invoice-form.html", context)

"""
#@login_required
def workorder_invoice_add_hx_view(request, parent_id= None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Workorder.objects.get(id=parent_id)
    except:
        parent_obj = None
    if parent_obj is  None:
        return HttpResponse("Not found.")

    instance = None
    if id is not None:
        print('1')
        try:
            print('2')
            instance = WorkorderInvoiceProduct.objects.get(workorder=parent_obj, id=id)
        except:
            print('3')
            instance = None
    form = WorkorderInvoiceForm(request.POST or None, instance=instance)
    url = reverse("workorders:hx-invoice-add", kwargs={"parent_id": parent_obj.id})
    if instance:
        url = instance.get_hx_edit_url()
    context = {
        "url": url,
        "form": form,
        "object": instance
    }
    if form.is_valid():
        new_obj=form.save(commit=False)
        if instance is None:
            new_obj.workorder = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "workorders/partials/invoice-inline.html", context) 
    return render(request, "workorders/partials/invoice-form.html", context)
"""


##Attempt at HTMX Dropdown
def customer(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'workorders/create-workorder.html', context)

#def customer(request):
#    form = WorkorderDynamicForm()
#    context = {'form': form}
#    return render(request, 'workorders/dynamiccustomer.html', context)

#def contacts(request):
#    form = WorkorderDynamicForm(request.GET)
#    #print(form['contact'])
#    return HttpResponse(form['contact'])

def create_base(request):
    context = {}
    if request.method == "GET":
        customers = Customer.objects.all()
        context = {'customers': customers}
        return render(request, 'workorders/create-workorder.html', context)
    print(request.POST)
    if request.method == "POST":
        customer = request.POST.get("customer")
        contact = request.POST.get("contact")
        workorder = request.POST.get("workorder")
        description = request.POST.get("description")
        deadline = request.POST.get("deadline")
        budget = request.POST.get("budget")
        quoted_price = request.POST.get("quoted_price")
        workorder = (workorder.upper())
        if customer == "0":
            customers = Customer.objects.all()
            context = {'customers': customers}
            context['error'] = 'Please select a customer'
            return render(request, 'workorders/create-workorder.html', context)
        if not workorder:
            customers = Customer.objects.all()
            context = {'customers': customers}
            context['workordererror'] = 'Please enter a workorder'
            return render(request, 'workorders/create-workorder.html', context)
        #if contact == 0: -- Contacts are optional at this point
        #    context['error']
        #    return render(request, 'workorders/create-workorder.html', context)   
        try:
            obj = Workorder.objects.create(customer_id=customer, contact_id=contact, workorder=workorder, description=description, deadline=deadline, budget=budget, quoted_price=quoted_price)
        except:
            customers = Customer.objects.all()
            context = {'customers': customers}
            context['workordererror'] = 'That workorder already exists'
            return render(request, 'workorders/create-workorder.html', context)
        context['workorder'] = workorder #return workorder number to form
        context['created'] = True
        return redirect(obj.get_edit_url())
    return render(request, "workorders/create-workorder.html", context=context)

def contacts(request):
    customer = request.GET.get('customer')
    contacts = Contact.objects.filter(customer=customer)
    context = {'contacts': contacts}
    return render(request, 'workorders/partials/contact-dropdown.html', context)

#def create_base(request):
#    customers = Customer.objects.all()
#    context = {'customers': customers}
#    return render(request, 'workorders/create-workorder.html', context)

def update_contact(request):
    customer = request.GET.get('customer')
    currentcontact = request.GET.get('contact')
    contacts = Contact.objects.filter(customer=customer)
    if currentcontact != 'None':
        currentcontact = Contact.objects.filter(id=currentcontact)
    if currentcontact == 'None':
        currentcontact = '0'
    context = {
        'contacts': contacts,
        'currentcontact': currentcontact
    }
    #print(contacts)
    #print(currentcontact)
    return render(request, 'workorders/partials/contact-update.html', context)

#def update_contact(request):
#    customer = request.GET.get('customer')
#    print(customer)
#    contacts = Contact.objects.filter(customer=customer)
#
#    context = {'contacts': contacts}
#    return render(request, 'workorders/partials/contact-update.html', context)
def service_detail(request):
    service = request.GET.get('item')
    obj = Service.objects.filter(name=service)
    context = {'objects': obj}
    return render(request, 'workorders/partials/service-detail.html', context)

def inventory_detail(request):
    inventory = request.GET.get('item')
    obj = Inventory.objects.filter(name=inventory)
    context = {'objects': obj}
    return render(request, 'workorders/partials/inventory-detail.html', context)

def workorder_service_detail(request, id=None):
    services = Service.objects.all().order_by('-name')
    form = WorkorderServiceForm(request.POST or None)
    item = request.GET.get('item')
    if item == '0':
        error = 'Please pick a Service'
        print(error)
        obj = ''
        #return render(request, 'workorders/partials/service-detail.html', context)
    if item != '0':
        obj = Service.objects.get(id=item)
        error = ''
    #parent_obj = Workorder.objects.get(id=parent_id)
    context = {
        'object': obj,
        'form': form,
        'services': services,
        'error': error
    }
    #print(obj.price)
    return render(request, 'workorders/partials/service-detail.html', context)

def workorder_inventory_detail(request, id=None):
    inventorys = Inventory.objects.all().order_by('-name')
    form = WorkorderInventoryForm(request.POST or None)
    item = request.GET.get('item')
    if item == '0':
        error = 'Please pick an Item'
        print(error)
        obj = ''
        #return render(request, 'workorders/partials/service-detail.html', context)
    if item != '0':
        obj = Inventory.objects.get(id=item)
        error = ''
    #parent_obj = Workorder.objects.get(id=parent_id)
    context = {
        'object': obj,
        'form': form,
        'inventorys': inventorys,
        'error': error
    }
    #print(obj.price)
    return render(request, 'workorders/partials/inventory-detail.html', context)