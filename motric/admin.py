from django.contrib import admin

# Register your models here.

from .models import *

def make_public(modeladmin, request, queryset):
    queryset.update(status='AVA')

def make_dedicated(modeladmin, request, queryset):
    queryset.update(status='ASS')

def make_requested(modeladmin, request, queryset):
    queryset.update(status='REQ')
    
make_public.short_description = "Make selected devices as PUBLIC"
make_dedicated.short_description = "Make selected devices as ASSIGNED"
make_requested.short_description = "Make selected devices as REQUESTED"

class RequesterAdmin(admin.ModelAdmin):
    list_display = ['ldap', 'cost_center', 'project', 'device_label']
    ordering = ['cost_center']

class RequestedDeviceAdmin(admin.ModelAdmin):
    list_display = ['model_type', 'quantity', 'os_version', 'requester', 'request_date', 'status']
    ordering = ['-request_date']
    actions = [make_public, make_dedicated, make_requested]

class LabDeviceAdmin(admin.ModelAdmin):
    list_display = ['model', 'device_id', 'os', 'project', 'owner', 'status', 'lab_location']
    ordering = ['-register_date']
    actions = [make_public, make_dedicated]
    fields = ('model', 'device_id', 'status', 'os', 'owner', 'user', 'label', 'project', 'lab_location')

admin.site.register(Requester, RequesterAdmin)
admin.site.register(RequestedDevice, RequestedDeviceAdmin)
admin.site.register(LabDevice, LabDeviceAdmin)
admin.site.register(Event)
