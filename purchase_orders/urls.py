from django.urls import path

from .views import (
    po_create_view,
    po_detail_view,
    po_detail_hx_view,
    po_list_view,
)

app_name='purchase_orders'
urlpatterns = [
    path("create-po/", po_create_view, name='create-po'),
    path("po/", po_list_view, name='po-list'),
    path("po/<int:id>/", po_detail_hx_view, name='hx-po-detail'),
    path("<int:id>/", po_detail_view, name='po-detail'),
]