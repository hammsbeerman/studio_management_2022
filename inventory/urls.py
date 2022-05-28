from django.urls import path

from .views import (
    category_list_view,
    mpn_create_view,
    mpn_list_view,
    mpn_detail_view,
    mpn_detail_hx_view,
    mpn_update_view,
    manufacturer_create_view,
    service_create_view,
    service_list_view,
    inventory_create_view,
    inventory_list_view,
    add_category_view,
    get_parent_view,
)

app_name='inventory'
urlpatterns = [
    path("create-mpn/", mpn_create_view, name='create-mpn'),
    path("add-manufacturer/", manufacturer_create_view, name='add-manufacturer'),
    path("add-service/", service_create_view, name='add-service'),
    path("service-list/", service_list_view, name='service-list'),
    path("add-inventory/", inventory_create_view, name='add-inventory'),
    path("inventory-list/", inventory_list_view, name='inventory-list'),
    path("mpn-list/", mpn_list_view, name='mpn-list'),
    path("mpn/<int:id>/", mpn_detail_hx_view, name='hx-mpn-detail'),
    path("<int:id>/", mpn_detail_view, name='mpn-detail'),
    path("<int:id>/edit", mpn_update_view, name='mpn-update'),
    path("add-category/", add_category_view, name='add-category'),
    path("add-category/getparent", get_parent_view, name='get-parent'),
    #path("", inventory_list_view, name='list'),
    #path("create/", customer_create_view, name='create'),
    #path("hx/<int:parent_id>/contacts/<int:id>/", customer_contact_update_hx_view, name='hx-contact-detail'),
    #path("hx/<int:parent_id>/contacts/", customer_contact_update_hx_view, name='hx-contact-create'),
    #path("hx/<int:id>/", customer_detail_hx_view, name='hx-detail'),
    #path("<int:id>/edit", customer_update_view, name='update'),
    #path("<int:id>/", inventory_detail_view, name='detail')
    #path("/ia/<int:parent>/", category_list_view, name='category-list') #Attmpting to get this to work
    path("admin/category/", category_list_view, name='category-list'), #Testing to get above to work
    path("admin/category/<int:parent>/", category_list_view, name='category-list'),
]