from . import views
from django.conf.urls import url
from django.views.generic.base import RedirectView

app_name = 'main'
urlpatterns = [

    # ajax url
    url(r'^ajax/request-networktype-info$', views.ajax_RequestNetworkTypeInfo, name='request-networktype-info'),
    url(r'^ajax/new-type-of-network$', views.ajax_NewTypeOfNetwork, name='new-type-of-network'),
    url(r'^ajax/create-network$', views.ajax_CreateNetwork, name='create-network'),
    url(r'^ajax/network-details-dashboard$', views.ajax_NetworkDetailsDashboard, name='network-details-dashboard'),
    url(r'^ajax/database-details$', views.ajax_DatabaseDetails, name='database-details'),
    url(r'^ajax/refresh-network-info$', views.ajax_RefreshNetworkInfo, name='refresh-network-info'),
    url(r'^ajax/delete-network$', views.ajax_DeleteNetwork, name='delete-network'),
    url(r'^ajax/create-database$', views.ajax_CreateDatabase, name='create-database'),
    url(r'^ajax/delete-database$', views.ajax_DeleteDB, name='delete-database'),
    url(r'^ajax/table-list$', views.ajax_TableList, name='table-list'),
    url(r'^ajax/close-db-connection$', views.ajax_CloseDB, name='close-db-connection'),

    # page url
    url(r'^dashboard/', views.DashboardView, name='dashboard'),
    url(r'^databases/browse', views.DatabasesBrowsingView, name='browse_databases'),
    url(r'^settings/general', views.GeneralSettingView, name='general_settings'),
    url(r'^settings/nettype', views.NettypeSettingsView, name='nettype_settings'),
    url(r'^$', RedirectView.as_view(pattern_name='main:dashboard'), name='go-to-dashboard'),
]
