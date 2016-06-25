from django.contrib import admin

# Register your models here.

from .models import *

def make_public(modeladmin, request, queryset):
    queryset.update(status='AVA')

def make_dedicated(modeladmin, request, queryset):
    queryset.update(status='ASS')
    
make_public.short_description = "Make selected devices as PUBLIC"
make_dedicated.short_description = "Make selected devices as ASSIGNED"

class RequesterAdmin(admin.ModelAdmin):
    list_display = ['ldap', 'cost_center', 'project', 'device_label']
    ordering = ['cost_center']

class RequestedDeviceAdmin(admin.ModelAdmin):
    list_display = ['model_type', 'quantity', 'os_version', 'requester', 'request_date', 'status']
    ordering = ['-request_date']
    actions = [make_public, make_dedicated]

class LabDeviceAdmin(admin.ModelAdmin):
    list_display = ['model', 'device_sn', 'status']
    ordering = ['model']
    actions = [make_public, make_dedicated]
    fields = ('model', 'device_sn', 'status')

admin.site.register(Requester, RequesterAdmin)
admin.site.register(RequestedDevice, RequestedDeviceAdmin)
admin.site.register(LabDevice, LabDeviceAdmin)
admin.site.register(Event)
