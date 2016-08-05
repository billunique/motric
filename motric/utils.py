from django.http import HttpResponse, HttpRequest, QueryDict
from django.shortcuts import render
from django.core.mail import send_mail
from django.utils import timezone
from models import *
import time, json


def expection_carrier():
    import sys
    dict = {}
    info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    dict['create_at'] = str(time.ctime())
    return json.dumps(dict)


def form_receiver(request):

    form_dict = request.POST.copy() # Interesting! This is naturally a dictionary (QueryDict), can be used for parse directly.  copy() is to make the dict mutable for pop().
    # return HttpResponse(form_querydict.items())  # return last value if the key has more than one value. (same key)
    # return HttpResponse(form_querydict.lists())  # return all values, as a list, for each member of the dict.
    #form_dict = form_querydict.lists() # don't use like this, will get a 'list indices must be integers not str' error.

    try:
        ldap = form_dict['requester']
        cost_center = form_dict['costcenter']
        project = form_dict['project']
        device_owner = form_dict['owner']
        device_label = form_dict['label']
        usr = Requester(ldap=ldap, cost_center=cost_center, project=project, device_owner=device_owner, device_label=device_label)
        usr.save()

        model_type = form_dict.pop('device') # list
        os_version = form_dict.pop('os') # list
        quantity = form_dict.pop('quantity') # list
        status = 'REQ'

        combo = ''
        for i in range(len(model_type)):
            rd = RequestedDevice(model_type=model_type[i], os_version=os_version[i], quantity=quantity[i], requester=usr, request_date=timezone.now(), status=status)
            rd.save()
            combo += ' * ' + model_type[i] + ' x ' + quantity[i] +'\n'

    except KeyError:
        return HttpResponse("No corresponding key found!")
    except ValueError: # invalid literal for int() with base 10: '' if only one line of device request submitted.
        pass
    except:
        return HttpResponse(expection_carrier())

    message = ldap + ' raised device request for:\n\n' + combo + '\n\nPlease go to http://motric.bej.corp.google.com:8083/request_disposal for details.'
    send_mail(
        '[Motric]Somebody raised device request!',
        message,
        'mobileharness.motric@gmail.com',
        # ['mobileharness-ops@google.com'],
        ['xiawang@google.com', 'yanyanl@google.com', 'ligang@google.com'],
        fail_silently=False
    )

    # return HttpResponse("Thanks for using Mobile Harness! We've received your request, if it's approved, we'll start purchasing shortly. Please stay tuned.")
    return render(request, 'motric_thanks.html')

def request_editor(request):
    message = ''
    if request.method == 'POST':
        message += 'request method is post\n'
        if request.is_ajax():
            message += 'this is indeed ajax!\n'

    dict = request.POST.copy()
    data = json.dumps(dict)
    message += data

    # try:
    pk = dict['pk']
    rd = RequestedDevice.objects.get(pk=pk)
    column = dict.values()[2]
    column_value = dict.values()[3]

    if column == 'po_number':
        rd.po_number = column_value
        rd.po_date = timezone.now()
        response = rd.po_number
    elif column == 'price_cny':
        rd.price_cny = column_value
        response = rd.price_cny
    elif column == 'price_usd':
        rd.price_usd = column_value
        response = rd.price_usd
    elif column == 'ex_rate':
        rd.ex_rate = column_value
        response = rd.ex_rate
    elif column == 'status':
        rd.status = column_value
        rd.resolved = True
        response = rd.status
    elif column == 'approve_date':
        rd.approve_date = timezone.now()
        response = rd.approve_date
    else:
        response = data
    rd.save()
    # except:
    #     return HttpResponse(expection_carrier())


    return HttpResponse(response)


def device_register(request):
    dict = request.POST.copy()
    try:
        pk = dict['pk'];
        rd = RequestedDevice.objects.get(pk=pk)
        serial_no = dict.pop('sn') # got a list of serial number;
        for i in range(len(serial_no)):
            ld = LabDevice(device_sn=serial_no[i], status='ASS', register_date=timezone.now(), model=rd) # LabDevice.model must be a RequestedDevice instance.
            ld.save()

    except:
        return HttpResponse(expection_carrier())

    return HttpResponse('saved successfully!')