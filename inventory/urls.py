from django.urls import path

from .views import (
    category_list_view,
    mpn_create_view,
    mpn_list_view,
    mpn_detail_view,
    mpn_detail_hx_view,
    mpn_update_view,
)

app_name='inventory'
urlpatterns = [
    path("create-mpn/", mpn_create_view, name='create-mpn'),
    path("mpn/", mpn_list_view, name='mpn-list'),
    path("mpn/<int:id>/", mpn_detail_hx_view, name='hx-mpn-detail'),
    path("<int:id>/", mpn_detail_view, name='mpn-detail'),
    path("<int:id>/edit", mpn_update_view, name='mpn-update'),
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