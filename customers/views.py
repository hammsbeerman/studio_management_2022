from multiprocessing import parent_process
from urllib.request import Request

from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory #modelform for querysets
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .models import Customer, Contact
from .forms import CustomerForm, CustomerContactForm
# Create your views here.

#@login_required
def customer_create_view(request):
    form = CustomerForm(request.POST or None)
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
    return render(request, "customers/add-update.html", context)


#@login_required
def customer_list_view(request):
    #qs = Customer.objects.filter(user=request.user)
    qs = Customer.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "customers/list.html", context)

#@login_required
def customer_detail_view(request, id=None):
    hx_url = reverse("customers:hx-detail", kwargs={"id": id})
    context = {
        "hx_url": hx_url
    }
    return render(request, "customers/detail.html", context)

#@login_required
def customer_detail_hx_view(request, id=None):
    if not request.htmx:
        #print("Here 1")
        raise Http404
    try:
        obj = Customer.objects.get(id=id)
    except:
        obj = None
    if obj is  None:
        return HttpResponse("Not found.")
    context = {
        "object": obj
    }
    return render(request, "customers/partials/detail.html", context) 

#@login_required
def customer_update_view(request, id=None):
    obj = get_object_or_404(Customer, id=id,)
    form = CustomerForm(request.POST or None, instance=obj) #instance=obj fills the form with data
    titles = ('true')
    new_contact_url = reverse("customers:hx-contact-create", kwargs={"parent_id": obj.id})
    CustomerContactFormset = modelformset_factory(Contact, form=CustomerContactForm, extra=0)
    qs = obj.contact_set.all()
    context = {
        "form": form,
        #"formset": formset,
        "object": obj,
        "new_contact_url": new_contact_url,
        "titles": titles,
    }
    #print(form)
    if all([form.is_valid()]):
    #if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        context['message'] = 'Data saved.'
    if request.htmx:
        return render(request, "customers/partials/forms.html", context)
    return render(request, "customers/add-update.html", context)

#@login_required
def customer_contact_update_hx_view(request, parent_id= None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Customer.objects.get(id=parent_id)
    except:
        parent_obj = None
    if parent_obj is  None:
        return HttpResponse("Not found.")

    instance = None
    if id is not None:
        try:
            instance = Contact.objects.get(customer=parent_obj, id=id)
        except:
            instance = None
    form = CustomerContactForm(request.POST or None, instance=instance)
    url = reverse("customers:hx-contact-create", kwargs={"parent_id": parent_obj.id})
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
            new_obj.customer = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "customers/partials/contact-inline.html", context) 
    return render(request, "customers/partials/contact-form.html", context)
