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
        ldap = form_dict.get('requester')
        cost_center = form_dict.get('costcenter')
        project = form_dict.get('project')
        device_owner = form_dict.get('owner')
        device_label = form_dict.get('label')
        comment = form_dict.get('comment')
        pref_loc = form_dict.get('pref_loc')
        usr = Requester(ldap=ldap, cost_center=cost_center, project=project, device_owner=device_owner, device_label=device_label, pref_location=pref_loc)
        # usr = Requester(ldap=ldap, cost_center=cost_center, project=project, device_owner=device_owner, device_label=device_label)
        usr.save()

        model_type = form_dict.pop('device') # list
        os_version = form_dict.pop('os') # list
        quantity = form_dict.pop('quantity') # list
        status = 'REQ'

        server = form_dict.get('svr')

        combo = ''
        for i in range(len(model_type)):
            rd = RequestedDevice(model_type=model_type[i], os_version=os_version[i], quantity=quantity[i], requester=usr, request_date=timezone.now(), comment=comment, status=status)
            rd.save()
            combo += ' * ' + model_type[i] + ' x ' + quantity[i] +'\n'

    except KeyError:
        return HttpResponse("No corresponding key found!")
    except ValueError: # invalid literal for int() with base 10: '' if only one line of device request submitted.
        pass
    except:
        return HttpResponse(expection_carrier())


    motric_host = "motric"
    subject = '[Motric]Somebody raised device request!'
    sender = 'mobileharness.motric@gmail.com'
    recipient = ['xiawang@google.com', 'yanyanl@google.com', 'ligang@google.com', 'jinrui@google.com', 'derekchen@google.com', 'joyl@google.com', 'nanz@google.com', 'magicpig@google.com', 'xmhu@google.com', 'dschlaak@google.com', 'ansalgado@google.com']
    # recipient = ['xiawang@google.com', 'yanyanl@google.com']
    cc_rcpt = ['mobileharness-ops@google.com']
    if server: # value is 't' (for test)
        motric_host = "xiawang.bej:8080"
        recipient = ['xiawang@google.com', 'yanyanl@google.com', 'ligang@google.com', 'jinrui@google.com', 'joyl@google.com']

    message = ldap + ' raised device request for:\n\n' + combo + '\n\nPlease go to http://' + motric_host + '/request_disposal/?f=req for details.'
    motric_send_mail(
        subject,
        message,
        sender,
        recipient, 
        cc_rcpt
    )

    # return HttpResponse("Thanks for using Mobile Harness! We've received your request, if it's approved, we'll start purchasing shortly. Please stay tuned.")
    return render(request, 'motric_thanks.html')


def log_generator(timestamp, operation, operator):
    evt_content = {'timestamp':timestamp, 'operation':operation, 'operator':operator}
    return evt_content


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
    pk = dict.get('pk')
    rd = RequestedDevice.objects.get(pk=pk)
    column = dict.values()[2]
    column_value = dict.values()[3]
    oldvalue = dict.get('ov')

    requester = rd.requester.ldap
    subject = "[Motric]Updates of your device request for mobile-harness"
    sender = 'mobileharness.motric@gmail.com'
    recipient = [requester + '@google.com']
    cc_rcpt = ['mobileharness-ops@google.com']

    # if column == 'po_number':
    #     rd.po_number = column_value
    # elif column == 'price_cny':
    #     rd.price_cny = column_value
    # elif column == 'price_usd':
    #     rd.price_usd = column_value
    # elif column == 'ex_rate':
    #     rd.ex_rate = column_value

    rd.__dict__[column] = column_value
    response = column_value

    if column == 'status':
        if column_value == 'REF': # status'value could be REF-refuse, ORD-ordered, etc.
            rd.resolved = True
            body = "Dear " + requester + ",\n\nWe're sorry that your device request for " + rd.model_type + " (quantity: " + str(rd.quantity) + ") is temporarily refused for some reason.\n" + "Please contact mobileharness-ops@goole.com for details."

        if column_value == 'APP':
            rd.approve_date = timezone.now();
            body = "Dear " + requester + ",\n\nThis is to inform you that your device request for " + rd.model_type + " (quantity: " + str(rd.quantity) + ") is approved.\n" + "We will start your purchase order shortly. Please stay tuned."

        if column_value == 'ORD': # this request is autoly submit after the po_number is inputted, so rd.po_number has gotten value.
            rd.po_date = timezone.now()
            # url = "https://pivt.googleplex.com/viewPo?poid=" + rd.po_number
            # body = "Dear " + requester + ",\n\nThis is to inform you that your device request for " + rd.model_type + " (quantity: " + str(rd.quantity) + ") is approved.\n" + "We have started your purchase order: " + url + " Please stay tuned."
            # body = "Dear " + requester + ",\n\nThis is to inform you that the purchase order for your request is raised.\n" + "You can check it here: " + url + " Looking forward to seeing you get and run these devices."
            body = "Dear " + requester + ",\n\nThis is to inform you that the purchase order for your request is raised.\nLooking forward to seeing you get and run these devices."

        if column_value == 'REC':
            rd.receive_date = timezone.now();
            url = "https://motric/details/?t=r&pk=" + pk
            body = "Hi Gang,\n\nThis is to inform you that the devices of request " + url + " already arrived.\n" + "Yanyan will hand them to you, please be ready to register them and make them online."
            recipient = ['ligang@google.com', 'yanyanl@google.com']
            cc_rcpt = ['xiawang@google.com', 'jinrui@google.com', 'derekchen@google.com', 'joyl@google.com', 'nanz@google.com']

        # email = EmailMessage(subject, body, sender, recipient, cc_rcpt, headers={'Cc': ','.join(cc_rcpt)})  # headers section must be included into the EmailMessage brackets.
        # email.send(fail_silently=False)
        motric_send_mail(subject, body, sender, recipient, cc_rcpt)
        column_value = rd.get_status_display()

    rd.save()

    event_msg = log_generator(timezone.now(), '<span class="">' + column + '</span> was changed from <span class="required">' + oldvalue + '</span> --> <span class="bold">' + column_value + '</span>', operator)
    evt = Event(request=rd, event=event_msg)
    evt.save()


    # except:
    #     return HttpResponse(expection_carrier())


    return HttpResponse(response)



def labdevice_editor(request):
    message = ''
    dict = request.POST.copy()
    data = json.dumps(dict)
    message += data

    pk = dict.get('pk')
    ld = LabDevice.objects.get(pk=pk)

    ## data is like this: {"pk": "191", "csrfmiddlewaretoken": "ZPUe3zv9snleUyycvG4Nr8UdlySz0iYD", "name": "os", "value": "Android 6.0.1", "ov": "Android 4.4.4"} ##
    field = dict.values()[2]
    field_value = dict.values()[3]
    oldvalue = dict.get('ov')

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
    pk = dict.get('pk')
    status = dict.get('status')
    rd = RequestedDevice.objects.get(pk=pk)
    event_msg = {}
    allocate_date = timezone.now()
    if status == 'LOC':
        rd.lab_location = dict['location']
    else:
        if status == 'CUR':
            ld_pk = dict.pop('pkid')
            for i in range(len(ld_pk)):
                ld = LabDevice.objects.get(pk=ld_pk[i])
                ld.owner = rd.requester.device_owner
                ld.label = rd.requester.device_label
                ld.project = rd.requester.project
                ld.status = 'ASS'
                # ld.respond_to.add(rd)
                rr = ResponseRelationship.objects.create(device=ld, request=rd, response_date=allocate_date)
                rr.save()
                ld.save()
                event_msg = log_generator(allocate_date, 'Made <span class="bold">' + ld.get_status_display() + '</span>, from public pool.', operator)
                evt = Event(device=ld, event=event_msg)
                evt.save()
            rd.status = 'ASS'
            event_msg_rd = log_generator(allocate_date, 'Resolved by allocating current devices from public pool to fulfill.', operator)
            evt_rd = Event(request=rd, event=event_msg_rd)
            evt_rd.save()
        else: # status is 'ASS' or 'AVA'
            # register_date = time.ctime()
            serial_no = dict.pop('did') # got a list of serial number;
            if status == 'AVA':
                rd.requester.device_owner = 'mobileharness'
                rd.requester.project = 'PUBLIC'
            for i in range(len(serial_no)):
                # ld = LabDevice(model=rd.model_type, device_id=serial_no[i], status=status, register_date=allocate_date, os=rd.os_version, owner=rd.requester.device_owner, label=rd.requester.device_label, project=rd.requester.project, lab_location=rd.lab_location) # LabDevice.model must be a RequestedDevice instance.
                ld = LabDevice(model=rd.model_type, device_id=serial_no[i], status=status, register_date=allocate_date, os=rd.os_version, owner=rd.requester.device_owner, label=rd.requester.device_label, project=rd.requester.project, lab_location=rd.lab_location, po_number=rd.po_number, po_date=rd.po_date, price_cny=rd.price_cny, price_usd=rd.price_usd) # Modified at 03/14/2017, to support registering device directly.
                ld.save()
                # ld.respond_to.add(rd)
                rr = ResponseRelationship.objects.create(device=ld, request=rd, response_date=allocate_date)
                rr.save()
                ld.save()
                event_msg = log_generator(allocate_date, 'Made <span class="bold">' + ld.get_status_display() + '</span>, from new purchase.', operator)
                evt = Event(device=ld, event=event_msg)
                evt.save()
            rd.status = status
            event_msg_rd = log_generator(allocate_date, 'Resolved by allocating newly purchased device to fulfill.', operator)
            evt_rd = Event(request=rd, event=event_msg_rd)
            evt_rd.save()
        rd.resolved = True
        rd.resolved_date = allocate_date
    rd.save()

    # except:
        # return HttpResponse(expection_carrier())

    return HttpResponse('Saved successfully!')
    # return HttpResponseRedirect('/request_disposal/')

def details(request):
    q = request.GET.copy()
    data = json.dumps(q)
    pk = q.get('pk')
    tp = q.get('t')
    # did = q['did']
    if tp == 'd': # query device
        ld = LabDevice.objects.get(pk=pk)
        did = ld.device_id
        first_response_target = RequestedDevice
        last_response_target = RequestedDevice
        # request_list = RequestedDevice.objects.filter(labdevice=pk).order_by('resolved_date')
        request_list = ld.respond_to.all().distinct()  ## Naturally this list is ordered by the response_date!;  distict() can elimilate the duplications. 
        if request_list: # http://stackoverflow.com/questions/53513/best-way-to-check-if-a-list-is-empty
            first_response_target = request_list[0]  ## But there is a KengDie design in django template, the .first .last (filter |first |last doesn't work - will raise a Negative Index Error) will re-sort the querySet by Objects' primary key, not the original position it's in the set. 
            last_response_target = request_list[len(request_list)-1]
        event_list = Event.objects.filter(device=ld)
        replacement_list = LabDevice.objects.filter(labdevice=pk)
        return render(request, 'motric_details_device.html', {'device':ld, 'did':did, 'request_list':request_list, 'first_target':first_response_target, 'last_target':last_response_target, 'event_list':event_list, 'replacement_list':replacement_list})
        # return render(request, 'motric_details_device.html', {'device':ld, 'did':did, 'request_list':request_list, 'event_list':event_list, 'replacement_list':replacement_list})
    if tp == 'r': # query request
        rd = RequestedDevice.objects.get(pk=pk)
        event_list = Event.objects.filter(request=rd)
        device_list = rd.labdevice_set.all().distinct()
        return render(request, 'motric_details_request.html', {'request':rd, 'device_list':device_list, 'event_list':event_list})


def device_replacement(request):
    p = request.POST.copy()
    data = json.dumps(p)
    pk = p.get('pk')
    repk = p.get('replacement_pk')
    ld_hold = LabDevice.objects.get(pk=pk)
    ld_attack = LabDevice.objects.get(pk=repk)
    replace_date = timezone.now()

    ld_hold.replaced_by.add(ld_attack)
    ld_hold.save()
    # rd = RequestedDevice.objects.filter(labdevice=repk)
    # event_hold = {'timestamp':replace_date, 'operation':'be replaced by device ' + rd[len(rd)-1].model_type +' (' + ld_attack.device_id +')', 'operator':operator}
    event_hold = log_generator(replace_date, 'be replaced by <a href="/details/?t=d&pk=' + str(ld_attack.id) + '" target="_blank">' + str(ld_attack) + '</a>', operator)
    event_attack = log_generator(replace_date, 'replaced <a href="/details/?t=d&pk=' + str(ld_hold.id) + '" target="_blank">' + str(ld_hold) + '</a>', operator)
    evt_hold = Event(device=ld_hold, event=event_hold)
    evt_attack = Event(device=ld_attack, event=event_attack)
    evt_hold.save()
    evt_attack.save()

    # rdl = RequestedDevice.objects.filter(labdevice=pk).order_by('resolved_date') # get the QuerySet of requesteddevice of the be_replaced device.  ## Bad criteria!
    # rdl = ld.respond_to.all().order_by('resolved_date')
    rrl = ResponseRelationship.objects.filter(device=pk).order_by('response_date')  ## actually the order_by section can be omitted.
    rd_last = rrl[len(rrl)-1].request # get the last object of the QuerySet, it's just the current requesteddevice that the be_replaced device are responding to. 
    # ld_attack.respond_to.add(rd_last)
    rr = ResponseRelationship.objects.create(device=ld_attack, request=rd_last, response_date=replace_date)
    rr.save()
    evt = Event(device=ld_attack, event=log_generator(replace_date, 'Request target added: <a href="/details/?t=r&pk=' + str(rd_last.id) + '" target="_blank">' + str(rd_last) + '</a>', operator))
    evt.save()

    owner_old = ld_attack.owner
    user_old = ld_attack.user
    label_old = ld_attack.label
    project_old = ld_attack.project
    status_old = ld_attack.status
    status_d = {'AVA':'Public', 'ASS':'Assigned', 'BRO':'Broken'}

    ld_attack.owner = ld_hold.owner
    ld_attack.user = ld_hold.user
    ld_attack.label = ld_hold.label
    ld_attack.project = ld_hold.project
    ld_attack.status = 'ASS'
    ld_attack.save()

    evt = Event(device=ld_attack, event=log_generator(replace_date, 'Properties are changed in bundle.<br/>' \
        + 'owner from <span class="required">' + owner_old + '</span> --> <b>' + ld_attack.owner + '</b>;<br/>' 
        + 'user from <span class="required">' + user_old + '</span> --> <b>' + ld_attack.user + '</b>;<br/>' \
        + 'label from <span class="required">' + label_old + '</span> --> <b>' + ld_attack.label + '</b>;<br/>' \
        + 'project from <span class="required">' + project_old + '</span> --> <b>' + ld_attack.project + '</b><br/>' \
        + 'status from <span class="required">' + status_d[status_old] + '</span> --> <b>' + ld_attack.get_status_display() + '</b>.', operator))
    evt.save()

    return HttpResponse(data)

def device_register(request):
    p = request.POST.copy()
    data = json.dumps(p)
    model = p.get('model')
    project = p.get('project')
    owner = p.get('owner')
    label = p.get('label')
    os = p.get('os')
    po_number = p.get('po_number')
    price_cn = p.get('price_cn')
    price_us = p.get('price_us')
    location = p.get('location')
    status = p.get('status')
    device_id = p.pop('device_id') # list

    for i in range(len(device_id)):
        ld = LabDevice(model=model, project=project, owner=owner, label=label, os=os, po_number=po_number, price_cny=price_cn, price_usd=price_us, lab_location=location, status=status, device_id=device_id[i])
        ld.save()

    return HttpResponse(data)