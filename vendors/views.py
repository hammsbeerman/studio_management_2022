from multiprocessing import parent_process
from socket import VM_SOCKETS_INVALID_VERSION
from urllib.request import Request

from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory #modelform for querysets
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .models import Vendor, VendorContact
from .forms import VendorForm, VendorContactForm

# Create your views here.

#@login_required
def vendor_create_view(request):
    form = VendorForm(request.POST or None)
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
    return render(request, "vendors/add-update.html", context)

#@login_required
def vendor_list_view(request):
    #qs = Vendor.objects.filter(user=request.user)
    qs = Vendor.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "vendors/list.html", context)

#@login_required
def vendor_detail_view(request, id=None):
    hx_url = reverse("vendors:hx-detail", kwargs={"id": id})
    context = {
        "hx_url": hx_url
    }
    return render(request, "vendors/detail.html", context)

#@login_required
def vendor_detail_hx_view(request, id=None):
    if not request.htmx:
        #print("Here 1")
        raise Http404
    try:
        obj = Vendor.objects.get(id=id)
    except:
        obj = None
    if obj is  None:
        return HttpResponse("Not found.")
    context = {
        "object": obj
    }
    return render(request, "vendors/partials/detail.html", context)

#@login_required
def vendor_update_view(request, id=None):
    obj = get_object_or_404(Vendor, id=id,)
    form = VendorForm(request.POST or None, instance=obj) #instance=obj fills the form with data
    titles = ('true')
    new_contact_url = reverse("vendors:hx-contact-create", kwargs={"parent_id": obj.id})
    VendorContactFormset = modelformset_factory(VendorContact, form=VendorContactForm, extra=0)
    qs = obj.vendorcontact_set.all()
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
        return render(request, "vendors/partials/forms.html", context)
    return render(request, "vendors/add-update.html", context)

#@login_required
def vendor_contact_update_hx_view(request, parent_id= None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Vendor.objects.get(id=parent_id)
    except:
        parent_obj = None
    if parent_obj is  None:
        return HttpResponse("Not found.")

    instance = None
    if id is not None:
        try:
            instance = Vendor.objects.get(vendor=parent_obj, id=id)
        except:
            instance = None
    form = VendorContactForm(request.POST or None, instance=instance)
    url = reverse("vendors:hx-contact-create", kwargs={"parent_id": parent_obj.id})
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
            new_obj.vendor = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "vendors/partials/contact-inline.html", context) 
    return render(request, "vendors/partials/contact-form.html", context)