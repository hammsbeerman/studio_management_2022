from django.urls import path

from .views import (
    vendor_list_view,
    vendor_create_view,
    vendor_detail_view,
    vendor_update_view,
    vendor_detail_hx_view,
    vendor_contact_update_hx_view,
)

app_name='vendors'
urlpatterns = [
    path("", vendor_list_view, name='list'),
    path("create/", vendor_create_view, name='create'),
    path("hx/<int:parent_id>/contacts/<int:id>/", vendor_contact_update_hx_view, name='hx-contact-detail'),
    path("hx/<int:parent_id>/contacts/", vendor_contact_update_hx_view, name='hx-contact-create'),
    path("hx/<int:id>/", vendor_detail_hx_view, name='hx-detail'),
    path("<int:id>/edit", vendor_update_view, name='update'),
    path("<int:id>/", vendor_detail_view, name='detail')
]