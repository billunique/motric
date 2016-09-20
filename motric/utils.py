from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage
from django.utils import timezone
from django.core import serializers
from models import *
import time, json, threading, getpass

operator = ''

def expection_carrier():
    import sys
    dict = {}
    info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    dict['create_at'] = str(time.ctime())
    return json.dumps(dict)

def who_are_you(request):
    p = request.POST.copy()
    data = json.dumps(p)
    who = p['operator']
    global operator
    operator = who
    return HttpResponse(data)


class EmailThread(threading.Thread):
    def __init__(self, subject, body, sender, recipient, cc_rcpt):
        self.subject = subject
        self.body = body
        self.sender = sender
        self.recipient = recipient
        self.cc_rcpt = cc_rcpt
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMessage(self.subject, self.body, self.sender, self.recipient, self.cc_rcpt, headers={'Cc': ','.join(self.cc_rcpt)})
        # msg.content_subtype = "html"
        msg.send(fail_silently=False)

def motric_send_mail(subject, body, sender, recipient, cc_rcpt):
    EmailThread(subject, body, sender, recipient, cc_rcpt).start()


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
        pref_loc = form_dict['pref_loc']
        usr = Requester(ldap=ldap, cost_center=cost_center, project=project, device_owner=device_owner, device_label=device_label, pref_location=pref_loc)
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
    motric_send_mail(
        '[Motric]Somebody raised device request!',
        message,
        'mobileharness.motric@gmail.com',
        ['xiawang@google.com', 'yanyanl@google.com', 'ligang@google.com'],
        ['mobileharness-ops@google.com']
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

    requester = rd.requester.ldap
    subject = "[Motric]Updates of your device request for mobile-harness"
    sender = 'mobileharness.motric@gmail.com'
    recipient = [requester + '@google.com']
    cc_rcpt = ['mobileharness-ops@google.com']

    response = column_value

    if column == 'po_number':
        rd.po_number = column_value
        rd.po_date = timezone.now()
    elif column == 'price_cny':
        rd.price_cny = column_value
    elif column == 'price_usd':
        rd.price_usd = column_value
    elif column == 'ex_rate':
        rd.ex_rate = column_value
    elif column == 'status':
        rd.status = column_value
        if column_value == 'REF': # status'value could be REF-refuse, ORD-ordered, etc.
            rd.resolved = True

            body = "Dear " + requester + ",\n\nWe're sorry that your device request for " + rd.model_type + " (quantity: " + str(rd.quantity) + ") is temporarily refused for some reason.\n" + "Please contact mobileharness-ops@goole.com for details."

        if column_value == 'ORD': # this request is autoly submit after the po_number is inputted, so rd.po_number has gotten value.
            url = "https://pivt.googleplex.com/viewPo?poid=" + rd.po_number
            body = "Dear " + requester + ",\n\nThis is to inform you that your device request for " + rd.model_type + " (quantity: " + str(rd.quantity) + ") is approved.\n" + "We have started your purchase order: " + url + " Please stay tuned."

        # email = EmailMessage(subject, body, sender, recipient, cc_rcpt, headers={'Cc': ','.join(cc_rcpt)})  # headers section must be included into the EmailMessage brackets.
        # email.send(fail_silently=False)
        motric_send_mail(subject, body, sender, recipient, cc_rcpt)

        response = requester +'\t' + rd.model_type +'\t' + rd.status
    elif column == 'approve_date':
        rd.approve_date = timezone.now()
    elif column == 'device_user':
        ld.user = column_value
    else:
        response = data
    rd.save()
    # except:
    #     return HttpResponse(expection_carrier())


    return HttpResponse(response)


def log_generator(timestamp, operation, operator):
    evt_content = {'timestamp':timestamp, 'operation':operation, 'operator':operator}
    return evt_content


def labdevice_editor(request):
    message = ''
    dict = request.POST.copy()
    data = json.dumps(dict)
    message += data

    pk = dict['pk']
    ld = LabDevice.objects.get(pk=pk)

    ## data is like this: {"pk": "191", "csrfmiddlewaretoken": "ZPUe3zv9snleUyycvG4Nr8UdlySz0iYD", "name": "os", "value": "Android 6.0.1", "ov": "Android 4.4.4"} ##
    field = dict.values()[2]
    field_value = dict.values()[3]
    oldvalue = dict['ov']

    # target = getattr(ld, field)
    # target = field_value
    ld.__dict__[field] = field_value
    ld.save()
    if field == 'status':
        field_value = ld.get_status_display()

    event_msg = log_generator(timezone.now(), '<span class="">' + field + '</span> was changed from <span class="required">' + oldvalue + '</span> --> <span class="bold">' + field_value + '</span>', operator)
    evt = Event(device=ld, event=event_msg)
    evt.save()
    message += "\n" + field + " " + field_value + " saved successfully."
    return HttpResponse(data, status=200, charset='utf8')


def device_allocate(request):
    dict = request.POST.copy()
    # try:
    pk = dict['pk']
    status = dict['status']
    rd = RequestedDevice.objects.get(pk=pk)
    register_date = timezone.now()
    # register_date = time.ctime()
    event_msg = {}
    if status == 'LOC':
        rd.lab_location = dict['location']
    elif status == 'CUR':
        ld_pk = dict.pop('pkid')
        for i in range(len(ld_pk)):
            ld = LabDevice.objects.get(pk=ld_pk[i])
            ld.owner = rd.requester.device_owner
            ld.label = rd.requester.device_label
            ld.project = rd.requester.project
            ld.status = 'ASS'
            ld.respond_to.add(rd)
            ld.save()
            event_msg = log_generator(register_date, 'made <span class="bold">' + ld.get_status_display() + '</span>', operator)
            evt = Event(device=ld, event=event_msg)
            evt.save()
        rd.resolved = True
    else: # status is 'ASS' or 'AVA'
        serial_no = dict.pop('did') # got a list of serial number;
        if status == 'AVA':
            rd.requester.device_owner = 'mobileharness'
            rd.requester.project = 'PUBLIC'
        for i in range(len(serial_no)):
            ld = LabDevice(model=rd.model_type, device_id=serial_no[i], status=status, register_date=register_date, os=rd.os_version, owner=rd.requester.device_owner, label=rd.requester.device_label, project=rd.requester.project) # LabDevice.model must be a RequestedDevice instance.
            ld.save()
            ld.respond_to.add(rd)
            ld.save()
            event_msg = log_generator(register_date, 'made <span class="bold">' + ld.get_status_display() + '</span>', operator)
            evt = Event(device=ld, event=event_msg)
            evt.save()
        rd.status = status
        rd.resolved = True
    rd.save()

    # except:
        # return HttpResponse(expection_carrier())

    return HttpResponse('Saved successfully!')
    # return HttpResponseRedirect('/request_disposal/')

def details(request):
    q = request.GET.copy()
    data = json.dumps(q)
    pk = q['pk']
    # did = q['did']
    ld = LabDevice.objects.get(pk=pk)
    did = ld.device_id
    request_list = RequestedDevice.objects.filter(labdevice=pk)
    event_list = Event.objects.filter(device=ld)
    replacement_list = LabDevice.objects.filter(labdevice=pk)
    return render(request, 'motric_details.html', {'device':ld, 'did':did, 'request_list':request_list, 'event_list':event_list, 'replacement_list':replacement_list})


def device_replacement(request):
    p = request.POST.copy()
    data = json.dumps(p)
    pk = p['pk']
    repk = p['replacement_pk']
    ld_hold = LabDevice.objects.get(pk=pk)
    ld_attack = LabDevice.objects.get(pk=repk)
    replace_date = timezone.now()

    ld_hold.replaced_by.add(ld_attack)
    ld_hold.save()
    # rd = RequestedDevice.objects.filter(labdevice=repk)
    # event_hold = {'timestamp':replace_date, 'operation':'be replaced by device ' + rd[len(rd)-1].model_type +' (' + ld_attack.device_id +')', 'operator':operator}
    event_hold = {'timestamp':replace_date, 'operation':'be replaced by <a href="/details/?pk=' + str(ld_attack.id) + '" target="_blank">' + str(ld_attack) + '</a>', 'operator':operator}
    event_attack = {'timestamp':replace_date, 'operation':'replaced <a href="/details/?pk=' + str(ld_hold.id) + '" target="_blank">' + str(ld_hold) + '</a>', 'operator':operator}
    evt_hold = Event(device=ld_hold, event=event_hold)
    evt_attack = Event(device=ld_attack, event=event_attack)
    evt_hold.save()
    evt_attack.save()

    rd = RequestedDevice.objects.filter(labdevice=pk) # get the QuerySet of requesteddevice of the be_replaced device.
    rd_last = rd[len(rd)-1] # get the last object of the QuerySet, it's just the current requesteddevice that the be_replaced device are responding.
    ld_attack.respond_to.add(rd_last)
    evt = Event(device=ld_attack, event=log_generator(replace_date, 'Request target added: <b>' + str(rd_last) + '</b>', operator))
    evt.save()

    owner_old = ld_attack.owner
    user_old = ld_attack.user
    label_old = ld_attack.label
    project_old = ld_attack.project

    ld_attack.owner = ld_hold.owner
    ld_attack.user = ld_hold.user
    ld_attack.label = ld_hold.label
    ld_attack.project = ld_hold.project
    ld_attack.save()

    evt = Event(device=ld_attack, event=log_generator(replace_date, 'Properties are changed in bundle.<br/>' \
        + 'owner from <span class="required">' + owner_old + '</span> --> <b>' + ld_attack.owner + '</b>;<br/>' 
        + 'user from <span class="required">' + user_old + '</span> --> <b>' + ld_attack.user + '</b>;<br/>' \
        + 'label from <span class="required">' + label_old + '</span> --> <b>' + ld_attack.label + '</b>;<br/>' \
        + 'project from <span class="required">' + project_old + '</span> --> <b>' + ld_attack.project + '</b>.', operator))
    evt.save()

    return HttpResponse(data)