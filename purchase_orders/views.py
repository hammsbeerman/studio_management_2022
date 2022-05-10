from django.urls import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .models import PurchaseOrder
from .forms import POForm

# Create your views here.
#Purchase Order Views

#@login_required
def po_create_view(request):
    form = POForm(request.POST or None)
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
    return render(request, "purchase_orders/add-update-po.html", context)

#@login_required
def po_detail_view(request, id=None):
    hx_url = reverse("purchase_orders:hx-po-detail", kwargs={"id": id})
    context = {
        "hx_url": hx_url
    }
    return render(request, "purchase_orders/po-detail.html", context)

#@login_required
def po_detail_hx_view(request, id=None):
    if not request.htmx:
        #print("Here 1")
        raise Http404
    try:
        obj = PurchaseOrder.objects.get(id=id)
    except:
        obj = None
    if obj is  None:
        return HttpResponse("Not found.")
    context = {
        "object": obj
    }
    return render(request, "purchase_orders/partials/po-detail.html", context) 

#@login_required
def po_list_view(request):
    #qs = Customer.objects.filter(user=request.user)
    qs = PurchaseOrder.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "purchase_orders/po-list.html", context)
