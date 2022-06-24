from django.urls import path

from .views import (
    customer_list_view,
    customer_create_view,
    customer_detail_view,
    customer_update_view,
    customer_detail_hx_view,
    customer_contact_update_hx_view,
    autosuggest,
)

app_name='customers'
urlpatterns = [
    path("", customer_list_view, name='list'),
    path("create/", customer_create_view, name='create'),
    path("name-autosuggest/", autosuggest, name='name-autosuggest'),
    path("hx/<int:parent_id>/contacts/<int:id>/", customer_contact_update_hx_view, name='hx-contact-detail'),
    path("hx/<int:parent_id>/contacts/", customer_contact_update_hx_view, name='hx-contact-create'),
    path("hx/<int:id>/", customer_detail_hx_view, name='hx-detail'),
    path("<int:id>/edit", customer_update_view, name='update'),
    path("<int:id>/", customer_detail_view, name='detail'),
]