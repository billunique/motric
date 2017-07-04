"""moha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from motric import views
from motric import utils

urlpatterns = [
    url(r'^$', views.index, name='index'),
	# url(r'^$', include('motric.urls')),
    url(r'^home/', views.home, name='home'),
    url(r'^labdevice/', views.labdevice, name='labdevice'),
    url(r'^public_device/', views.public_device, name='public'),
    url(r'^dedicated_device/', views.dedicated_device, name='dedicated'),
    url(r'^broken_device/', views.broken_device, name='broken'),
    url(r'^device_request/', views.device_request, name='request'),
    url(r'^request_disposal/', views.request_disposal, name='req_disposal'),
    url(r'^request_history/*', views.request_history, name='req_history'),
    url(r'^device_register/', views.device_register, name='dev_register'),

    # url(r'^faq/', views.faq, name='faq'),
    # url(r'^about/', views.about, name='about'),
	url(r'^request/', utils.form_receiver, name='receiver'), # this is a pratical technic.
    url(r'^edit_request/', utils.request_editor, name='req_editor'),
    url(r'^device_allocate/', utils.device_allocate, name='dev_allocate'),
    url(r'^edit_labdevice/', utils.labdevice_editor, name='labd_editor'),

    url(r'^details/', utils.details, name='details'),
    url(r'^my_tasks/*', utils.my_request, name='my_request'),
    url(r'^search/', utils.search, name='search'),
    url(r'^device_replacement/', utils.device_replacement, name='replacement'),
    url(r'^register/', utils.device_register, name='labd_register'),
    url(r'^mal_record/', utils.malfunction_record, name='mal_record'),
    url(r'^mal_statistics/', utils.malfunction_statistics, name='mal_statistics'),

    url(r'^who/', utils.who_are_you, name='who'),
    url(r'^sync_info/', utils.syncer, name='sync_info'),
    url(r'^response_status/', utils.response_checker, name='response_checker'),
    url(r'^import_data/', utils.import_sheet, name='data_importor'),
    url(r'^admin/', admin.site.urls),
]

# Customize the header title of the admin site.
admin.site.site_header = 'Motric administration'