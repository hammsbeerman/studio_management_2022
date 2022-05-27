from django.urls import path

from .views import (
    workorder_list_view,
    #workorder_create_view,
    workorder_detail_view,
    workorder_detail_hx_view,
    workorder_update_view,
    workorder_inventory_update_hx_view,
    workorder_noninventory_update_hx_view,
    workorder_service_update_hx_view,
    create_base,
    contacts,
    update_contact,
    #custom_workorder_create,
    service_detail,
    workorder_service_detail
    
)

app_name='workorders'
urlpatterns = [
    path("", workorder_list_view, name='list'), #List All workorders
    path("createbase/", create_base, name='createbase'), #Create base details of new workorder
    path('contacts/', contacts, name='contacts'), #Fills the contact dropdown on createbase/
    path('updatecontact/', update_contact, name='update-contact'), ####
    path('servicedetail/', service_detail, name='service-detail'),
    #path("custom/", custom_workorder_create, name='custom'), #Calls save method for createbase/
    #path("create/", workorder_create_view, name='create'), #Should be obsolete, replaced by createbase/
    path("hx/<str:parent_id>/inventory/", workorder_inventory_update_hx_view, name='hx-inventory-create'),
    path("hx/<str:parent_id>/inventory/<int:id>/", workorder_inventory_update_hx_view, name='hx-workorder-inventory-detail'),
    path("hx/<str:parent_id>/noninventory/", workorder_noninventory_update_hx_view, name='hx-noninventory-create'),
    path("hx/<str:parent_id>/noninventory/<int:id>/", workorder_noninventory_update_hx_view, name='hx-workorder-noninventory-detail'),
    path("hx/<str:parent_id>/service/", workorder_service_update_hx_view, name='hx-service-create'),
    path("hx/<str:parent_id>/service/<int:id>/", workorder_service_update_hx_view, name='hx-workorder-service-detail'),
    path("hx/<str:id>/", workorder_detail_hx_view, name='hx-detail'),
    path("<str:id>/servicedetail", workorder_service_detail, name='service-detail'),
    path("<str:id>/edit", workorder_update_view, name='update'),
    path("<str:id>/", workorder_detail_view, name='detail'),

    
]