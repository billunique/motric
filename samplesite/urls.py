"""samplesite URL Configuration

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
from motric import form_receiver

urlpatterns = [
    url(r'^$', views.index, name='index'),
	# url(r'^$', include('motric.urls')),
    url(r'^home/', views.home, name='home'),
    url(r'^device_request/', views.device_request, name='request'),
    url(r'^device_disposal/', views.device_disposal, name='disposal'),
    url(r'^faq/', views.faq, name='faq'),
    url(r'^about/', views.about, name='about'),
	url(r'^request/', form_receiver.jsonReceiver, name='receiver'), # this is a pratical technic.
	url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
]
