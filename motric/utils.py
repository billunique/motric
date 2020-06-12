from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage
from django.utils import timezone
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncMonth, ExtractMonth, ExtractYear
from collections import Counter
import json, threading, shlex, socket, operator, random, gviz_api
from models import *

loginer = ''

motric_host = "motric"
sender = 'mobileharness.motric@gmail.com'
recipient = []
# recipient = ['xiawang@google.com', 'yanyanl@google.com', 'ligang@google.com', 'jinrui@google.com', 'derekchen@google.com', 'joyl@google.com', 'nanz@google.com', 'magicpig@google.com', 'xmhu@google.com', 'dschlaak@google.com', 'ansalgado@google.com']
cc_rcpt = ['mobileharness-ops@google.com', 'mobileharness-ops-mtv@google.com']
# cc_rcpt = ['magicpig@google.com', 'xmhu@google.com', 'dschlaak@google.com', 'ansalgado@google.com', 'ffeng@google.com']

if 'mhl040' not in socket.gethostname(): # clumsy change: motric->mhl040, due to reimaging mhl040 to serve as motric server.
    motric_host = "xiawang.bej:8080"
    recipient = ['xiawang@google.com']
    cc_rcpt = ['yanyanl@google.com', 'xiawang@google.com']


def expection_carrier():
    import sys, time
    dict = {}
    info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    dict['create_at'] = str(time.ctime())
    return json.dumps(dict)

def who_are_you(request):
    p = request.POST.copy()
    data = json.dumps(p)
    who = p.get('operator')
    global loginer
    loginer = who
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
        msg.content_subtype = "html"
        msg.send(fail_silently=False)

def motric_send_mail(subject, body, sender, recipient, cc_rcpt):
    EmailThread(subject, body, sender, recipient, cc_rcpt).start()

def fancy_name(name):
    color_list = ['#4285F4', '#EA4335', '#FBBC05', '#34A853']
    user = '<b>'
    for c in name:
        user += '<span style="color:' + random.choice(color_list) +'">' + c + '</span>'
    user += '</b>'
    return user

def form_receiver(request):

    form_dict = request.POST.copy() # Interesting! This is naturally a dictionary (QueryDict), can be used for parse directly.  copy() is to make the dict mutable for pop().
    # return HttpResponse(form_querydict.items())  # return last value if the key has more than one value. (same key)
    # return HttpResponse(form_querydict.lists())  # return all values, as a list, for each member of the dict.
    #form_dict = form_querydict.lists() # don't use like this, will get a 'list indices must be integers not str' error.

    try:
        bug_id = form_dict.get('bug_id')
        ldap = form_dict.get('requester')
        cost_center = form_dict.get('costcenter')
        project = form_dict.get('project')
        device_owner = form_dict.get('owner')
        device_label = form_dict.get('label')
        comment = form_dict.get('comment')
        pref_loc = form_dict.get('pref_loc')
        usr = Requester(bug_id=bug_id, ldap=ldap, cost_center=cost_center, project=project, device_owner=device_owner, device_label=device_label, pref_location=pref_loc)
        # usr = Requester(ldap=ldap, cost_center=cost_center, project=project, device_owner=device_owner, device_label=device_label)
        usr.save()

        model_type = form_dict.pop('device') # list
        os_version = form_dict.pop('os') # list
        quantity = form_dict.pop('quantity') # list
        used_for = form_dict.getlist('used_for')
        status = 'REQ'
        server = form_dict.get('svr')

        combo = '<table cellpadding="3" border="1" style="border:2px solid gray; border-collapse:collapse">'
        subject = '[Motric]New device request received!'
        global motric_host, recipient, cc_rcpt  # mysteriuos, no need to global copy the variable sender, guess it's defined by the settings.py and be used globally.
        # if server: # value is 't' (for test)
        #     motric_host = "xiawang.bej:8080"
        #     recipient = ['xiawang@google.com']

        for i in range(len(model_type)):
            rd = RequestedDevice(model_type=model_type[i], os_version=os_version[i], quantity=quantity[i], requester=usr, request_date=timezone.now(), comment=comment, status=status, bug_id=bug_id)
            if usr.pref_location == 'MTV':
                rd.lab_location = 'MTV'
                rd.assignee = 'ffeng'
            if usr.pref_location == 'PEK':
                rd.assignee = 'yanyanl'
            rd.save()
            for x in range(len(used_for)):
                ug = Usage(request=rd, used_for=used_for[x])
                ug.save()
            # combo += ' * ' + model_type[i] + ' x ' + quantity[i] +'\t<span style="float:right">http://' + motric_host + '/details/?t=r&pk=' + str(rd.pk) + '</span><br/>'
            combo += '<tr><td>' + model_type[i] + ' * ' + quantity[i] + ' at ' + rd.lab_location + ' lab</td><td>http://' + motric_host + '/details/?t=r&pk=' + str(rd.pk) + '</td></tr>'
        combo += '</table>'


    except KeyError:
        return HttpResponse("No corresponding key found!")
    except IndexError:
        return HttpResponse("You might input something which causes the list index out of range, please check and try again.")
    except ValueError: # invalid literal for int() with base 10: '' if only one line of device request submitted.
        pass
    # except:
    #     return HttpResponse(expection_carrier())

    recipient = [ldap + '@google.com']

    message = 'Dear ' + fancy_name(ldap) + ',<br/><br/>We have received your device request for:<br/><br/>' + combo + '<p>Please see <a href="https://docs.google.com/document/d/1x-0ldb9j1vmDX7YVGJuEwKqsZEzgpqPN8E7rnIwzY8g/edit#heading=h.yvtx8zw2ebuj" target="_blank"><i><b>Mobile Harness Device Procurement and Preparation SLA</b></i></a> to expect the ETA.</p><p>Basically we will inform you if there are any update on your request, <br/>you can also go to http://' + motric_host + '/search/?q=requester:' + ldap + ' to check current status of the requests under your name.</p>'

    message += '<br/><p>Best regards,<br/>Mobile Harness team</p>'

    motric_send_mail(
        subject,
        message,
        sender,
        recipient, 
        cc_rcpt
    )

    # return HttpResponse("Thanks for using Mobile Harness! We've received your request, if it's approved, we'll start purchasing shortly. Please stay tuned.")
    return render(request, 'motric_thanks.html')

def quota_collect(request):

    subject = '[Motric]New quota device request received!'
    combo = '<table cellpadding="3" border="1" style="border:2px solid gray; border-collapse:collapse">'

    form_dict = request.POST.copy()
    try:
        ldap = form_dict.get('quota_requester')
        mdb = form_dict.get('mdbgroup')
        pe = form_dict.get('pes')
        # pe_poc = form_dict.get('pe_poc')
        comment = form_dict.get('comment')
        request_date=timezone.now()
        shared_device = form_dict.getlist('shared_device')
        model_type = form_dict.pop('device') # list
        os_version = form_dict.pop('os') # list
        quantity = form_dict.pop('quantity') # list

        global motric_host, recipient, cc_rcpt  # mysteriuos, no need to global copy the variable sender, guess it's defined by the settings.py and be used globally

        if shared_device: # list is not empty
            for i in range(len(shared_device)):
                qd = QuotaDevice(ldap=ldap, mdb=mdb, pe=pe, comment=comment, shared_device=shared_device[i], request_date=request_date)
                qd.save()
                combo += '<tr><td>' + shared_device[i] + ' for ' + pe + ', ' + comment + '</td></tr>'


        if model_type: # list is not empty
            for i in range(len(model_type)):
                qd = QuotaDevice(ldap=ldap, mdb=mdb, pe=pe, comment=comment, model_type=model_type[i], os_version=os_version[i], quantity=quantity[i], request_date=request_date)
                qd.save()
                combo += '<tr><td>' + model_type[i] + ' * ' + quantity[i] + ' for ' + pe + ', ' + comment + '</td></tr>'

    except KeyError:
        return HttpResponse("No corresponding key found!")
    except IndexError:
        return HttpResponse("You might input something which causes the list index out of range, please check and try again.")
    except ValueError: # invalid literal for int() with base 10: '' if only one line of device request submitted.
        pass
    # except:
    #     return HttpResponse(expection_carrier())

    combo += '</table>'
    message = 'Dear ' + fancy_name(ldap) + ',<br/><br/>We have received your device quota request for:<br/><br/>' + combo 
    message += '<br/><p>Best regards,<br/>Mobile Harness team</p>'
    recipient = [ldap + '@google.com']

    motric_send_mail(
        subject,
        message,
        sender,
        recipient, 
        cc_rcpt
    )

    return HttpResponse(message)
    return render(request, 'motric_thanks.html')


def log_generator(timestamp, operation, operator):
    evt_content = {'timestamp':timestamp, 'operation':operation, 'operator':operator}
    return evt_content


def request_editor(request):

    p = request.POST.copy()
    data = json.dumps(p)

    # try:
    pk = p.get('pk')
    rd = RequestedDevice.objects.get(pk=pk)
    column = p.get('name')
    column_value = p.get('value')
    oldvalue = p.get('ov')
    operator = p.get('opt')
    reason = p.get('reason')
    eta = p.get('eta')

    requester = rd.requester.ldap
    subject = "[Motric]Updates of your device request for mobile-harness"
    recipient = [requester + '@google.com']

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

    url = "http://" + motric_host + "/details/?t=r&pk=" + pk
    if column == 'status':
        if column_value == 'REF': # status'value could be REF-refuse, ORD-ordered, etc.
            rd.resolved = True
            body = "Dear " + fancy_name(requester) + ",<br/><br/>We're sorry that your device request for " + rd.model_type + " * " + str(rd.quantity) + " (" + url + ") is temporarily refused for the reason: <b>" + reason + "</b><br/><br/>You can contact mobileharness-ops@goole.com for details."

        if column_value == 'APP':
            rd.approve_date = timezone.now();
            body = "Dear " + fancy_name(requester) + ",<br/><br/>This is to inform you that your device request for " + rd.model_type + " * " + str(rd.quantity) + " (" + url + ") is approved. <br/>Hopefully it will be fulfilled by <b>" + str(eta) + "</b> (estimated). We will start your purchase order shortly. Please stay tuned."

        if column_value == 'ORD': # this request is autoly submit after the po_number is inputted, so rd.po_number has gotten value.
            rd.po_date = timezone.now()
            # url = "https://pivt.googleplex.com/viewPo?poid=" + rd.po_number
            # body = "Dear " + requester + ",<br/><br/>This is to inform you that your device request for " + rd.model_type + " (quantity: " + str(rd.quantity) + ") is approved.<br/>" + "We have started your purchase order: " + url + " Please stay tuned."
            # body = "Dear " + requester + ",<br/><br/>This is to inform you that the purchase order for your request is raised.<br/>" + "You can check it here: " + url + " Looking forward to seeing you get and run these devices."
            body = "Dear " + fancy_name(requester) + ",<br/><br/>This is to inform you that the purchase order of your request for " + rd.model_type + " * " + str(rd.quantity) + " (" + url + ") is raised.<br/>Looking forward to seeing you get and run these devices on Mobile Harness."

        if column_value == 'REC':
            rd.receive_date = timezone.now();
            # body = "Dear " + requester + ",<br/><br/>This is to inform you that the devices of request " + url + " already arrived.<br/>" + "Yanyan will hand them to you, please be ready to register them and make them online."
            body = "Dear " + fancy_name(requester) + ",<br/><br/>This is to inform you that the devices of your request for " + rd.model_type + " * " + str(rd.quantity) + " (" + url + ")  already arrived.<br/>" + "We will set up and make them online soon, and will inform you once they are ready."

        body += "<br/><p>Best regards,<br/>Mobile Harness team</p>"
        column_value = rd.get_status_display()
        motric_send_mail(subject, body, sender, recipient, cc_rcpt)

    if column == 'assignee':
        subject = "[Motric]" + str(rd)
        ase = column_value
        recipient = [ase + '@google.com']
        body = url + "<br/><br/>"  + "</p><br/><span style='color:#999999'>request:</span> " + str(rd) + "<br/><span style='color:#999999'>status: </span>" + rd.get_status_display() \
        + "<p><br/>" + operator + "@google.com <b>Changed</b><br/><span style='color:#999999'>assignee:</span> " + oldvalue + " &rarr; " + ase + "</p>" \
        # + "<p>Hi " + ase +", you are set to be assignee for this request, please check what will you do next. Thanks!"
        
        
       

        # email = EmailMessage(subject, body, sender, recipient, cc_rcpt, headers={'Cc': ','.join(cc_rcpt)})  # headers section must be included into the EmailMessage brackets.
        # email.send(fail_silently=False)
        motric_send_mail(
            subject, 
            body, 
            sender, 
            recipient, 
            cc_rcpt
        )
        

    rd.save()

    event_msg = log_generator(timezone.now(), '<span class="">' + column + '</span> was changed from <span class="required">' + oldvalue + '</span> --> <span class="bold">' + column_value + '</span>', operator)
    evt = Event(request=rd, event=event_msg)
    evt.save()

    if eta:
        rd.eta_date = eta
        rd.save()
        event_msg = log_generator(timezone.now(), 'Estimated completion day was set to <span class="required">' + eta + '</span>.' , operator)
        evt = Event(request=rd, event=event_msg)
        evt.save()


    # except:
    #     return HttpResponse(expection_carrier())


    return HttpResponse(data)



def labdevice_editor(request):
    p = request.POST.copy()
    data = json.dumps(p)

    pk = p.get('pk')
    ld = LabDevice.objects.get(pk=pk)

    ## data is like this: {"pk": "191", "csrfmiddlewaretoken": "ZPUe3zv9snleUyycvG4Nr8UdlySz0iYD", "name": "os", "value": "Android 6.0.1", "ov": "Android 4.4.4"} ##
    field = p.get('name')
    field_value = p.get('value')
    oldvalue = p.get('ov')
    operator = p.get('opt')

    # target = getattr(ld, field)
    # target = field_value
    ld.__dict__[field] = field_value
    ld.save()
    if field == 'status':
        field_value = ld.get_status_display()

    event_msg = log_generator(timezone.now(), '<span class="">' + field + '</span> was changed from <span class="required">' + oldvalue + '</span> --> <span class="bold">' + field_value + '</span>', operator)
    evt = Event(device=ld, event=event_msg)
    evt.save()
    return HttpResponse(data)


def device_allocate(request):
    dict = request.POST.copy()
    # try:
    pk = dict.get('pk')
    status = dict.get('status')
    operator = dict.get('opt')
    rd = RequestedDevice.objects.get(pk=pk)
    response_qty = rd.responserelationship_set.all().count()
    required_qty = rd.quantity - response_qty
    event_msg = {}
    allocate_date = timezone.now()
    # if status == 'LOC':
    #     rd.lab_location = dict['location']
    # else:
    
    duplicates = []
    if status == 'CUR':
        price_cny_sum = 0
        price_usd_sum = 0
        po_number = []
        ld_dict = {}
        ld_pk = dict.getlist('pkid')
        for i in range(len(ld_pk)):
            ld = LabDevice.objects.get(pk=ld_pk[i])
            ld_dict[ld_pk[i]]=ld.device_id
            price_cny_sum += int(ld.price_cny or 0)
            price_usd_sum += int(ld.price_usd or 0)
            ld_po_number = str(ld.po_number or '')
            if ld_po_number not in po_number:
                po_number.append(ld_po_number)
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

        event_msg_rd = log_generator(allocate_date, 'Allocate current devices from public pool: <br/>' \
            + json.dumps(ld_dict), operator)
        if len(ld_pk) == required_qty:
            rd.status = 'ASS'
            rd.resolved = True
            rd.resolved_date = allocate_date
            rd.price_cny = price_cny_sum / len(ld_pk)
            rd.price_usd = price_usd_sum / len(ld_pk)
            rd.po_number = ",".join(po_number)
            event_msg_rd = log_generator(allocate_date, 'Resolved by allocating current devices from public pool to fulfill: <br/>' \
            + json.dumps(ld_dict), operator)

        evt_rd = Event(request=rd, event=event_msg_rd)
        evt_rd.save()
    else: # status is 'ASS' or 'AVA'
        lds = LabDevice.objects.all()
        id_list = [e.device_id for e in lds]
        device_list = []
        serial_no = dict.getlist('did') # got a list of serial number;
        if status == 'AVA':
            rd.requester.device_owner = 'mobileharness'
            rd.requester.project = 'PUBLIC'
        for i in range(len(serial_no)):  ##------------------------------ This section learns from function device_register().
            if serial_no[i] not in id_list:
                device_list.append(serial_no[i])
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
            else:
                register_id = lds.get(device_id=serial_no[i]).id
                duplicates.append(serial_no[i] + ' (#' + str(register_id) + ')')

        if device_list != []:
            event_msg_rd = log_generator(allocate_date, 'Allocate newly purchased device: <br/>' \
                + json.dumps(device_list), operator)
        else:
            event_msg_rd = log_generator(allocate_date, 'Allocating duplications, allocation failed.', operator)

        if duplicates == []:
            if len(serial_no) == required_qty:
                rd.status = status
                rd.resolved = True
                rd.resolved_date = allocate_date
                event_msg_rd = log_generator(allocate_date, 'Resolved by allocating newly purchased device to fulfill: <br/>' \
                + json.dumps(device_list), operator)
        evt_rd = Event(request=rd, event=event_msg_rd)
        evt_rd.save()
    rd.save()

    if rd.resolved:
        requester = rd.requester.ldap
        subject = '[Motric]Updates of your device request for mobile-harness'
        recipient = [requester  + '@google.com']
        url = "http://" + motric_host + "/details/?t=r&pk=" + pk

        id_comb = ''
        lds_resp = LabDevice.objects.filter(respond_to=rd)
        for e in lds_resp:
            id_comb += e.device_id + '|'
        id_comb = id_comb[:-1]  # trim the last "|"
        moha_url = 'https://mobileharness.corp.google.com/lab.html#subpage=DEVICE_SEARCH&q=id:' + id_comb
        
        message = "Dear " + fancy_name(requester) + ",<br/><br/>This is to inform you that your device request for " + rd.model_type + " * " + str(rd.quantity) + " (" + url + ") is fulfilled.<br/>" + "The devices have been set up, please check here:" + moha_url + "<br/><br/>Thank you for using Mobile Harness and happy playing!<br/><p>Best regards,<br/>Mobile Harness team</p>"

        motric_send_mail(
            subject,
            message,
            sender,
            recipient, 
            cc_rcpt
        )


    # except:
        # return HttpResponse(expection_carrier())

    return HttpResponse(json.dumps(duplicates))
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
        replacement_to_list = LabDevice.objects.get(pk=pk).labdevice_set.all()
        mf = MalFunction.objects.filter(device=ld)
        lst = [e.get_type_display() for e in mf]
        mf_dict = dict(Counter(lst))
        items_lst = sorted(mf_dict.items(), key=lambda pair:pair[1], reverse=True)
        return render(request, 'motric_details_device.html', {'device':ld, 'did':did, 'request_list':request_list, 'first_target':first_response_target, 'last_target':last_response_target, 'event_list':event_list, 'replacement_list':replacement_list, 'replacement_to_list':replacement_to_list, 'type_count_list':items_lst})
        # return render(request, 'motric_details_device.html', {'device':ld, 'did':did, 'request_list':request_list, 'event_list':event_list, 'replacement_list':replacement_list})
    if tp == 'r': # query request
        rd = RequestedDevice.objects.get(pk=pk)
        ug = Usage.objects.filter(request=rd)
        event_list = Event.objects.filter(request=rd)
        device_list = rd.labdevice_set.all().distinct()
        return render(request, 'motric_details_request.html', {'request':rd, 'usage':ug, 'device_list':device_list, 'event_list':event_list})


def device_replacement(request):
    p = request.POST.copy()
    data = json.dumps(p)
    pk = p.get('pk')
    repk = p.get('replacement_pk')
    operator = p.get('opt')
    ld_hold = LabDevice.objects.get(pk=pk)
    ld_attack = LabDevice.objects.get(pk=repk)
    replace_date = timezone.now()

    ld_hold.replaced_by.add(ld_attack)
    ld_hold.replaced = 1
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
    if rrl:
        rd_last = rrl[len(rrl)-1].request # get the last object of the QuerySet, it's just the latest request that the be_replaced device are responding to.
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
        + 'owner from <span class="required">' + str(owner_old) + '</span> --> <b>' + str(ld_attack.owner) + '</b>;<br/>' 
        + 'user from <span class="required">' + str(user_old) + '</span> --> <b>' + str(ld_attack.user) + '</b>;<br/>' \
        + 'label from <span class="required">' + str(label_old) + '</span> --> <b>' + str(ld_attack.label) + '</b>;<br/>' \
        + 'project from <span class="required">' + str(project_old) + '</span> --> <b>' + str(ld_attack.project) + '</b>;<br/>' \
        + 'status from <span class="required">' + status_d[status_old] + '</span> --> <b>' + ld_attack.get_status_display() + '</b>.' \
        , operator))
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
    operator = p.get('opt')

    lds = LabDevice.objects.all()
    id_list = [e.device_id for e in lds]
    duplicates = []
    for i in range(len(device_id)):
        if device_id[i] not in id_list:  # Looks like it's not a performance-killer.
            ld = LabDevice(model=model, project=project, owner=owner, label=label, os=os, po_number=po_number, price_cny=price_cn, price_usd=price_us, lab_location=location, status=status, device_id=device_id[i])
            ld.save()
            evt = Event(device=ld, event=log_generator(ld.register_date, 'Device registered directly.', operator))
            evt.save()
        else:
            register_id = lds.get(device_id=device_id[i]).id
            duplicates.append(device_id[i] + ' (#' + str(register_id) + ')')
    return HttpResponse(json.dumps(duplicates))


def syncer(request):
    p = request.POST.copy()
    data = json.dumps(p)
    pk = p.get('pk')
    target = p.get('name')
    sync_value = p.get('value')
    operator = p.get('opt')
    ld_set = LabDevice.objects.filter(respond_to=pk)
    if target == 'po':
        po_date = timezone.now()
        rd = RequestedDevice.objects.get(pk=pk)
        rd.po_date = po_date
        rd.save()
        for ld in ld_set:
            old_po = ld.po_number
            ld.po_number = sync_value
            ld.po_date = po_date
            ld.save()
            evt = Event(device=ld, event=log_generator(timezone.now(), 'PO number synced from <span class="required">' + old_po + '</span> --> <b>' + sync_value +'</b>.', operator))
            evt.save()

    return HttpResponse(data)

def response_checker(request):
    p = request.POST.copy()
    pk = p.get('pk')
    ld_set = LabDevice.objects.filter(respond_to=pk)
    did_list = []
    for ld in ld_set:
        device_item = ld.device_id + ' (#' + str(ld.id) + ')'
        did_list.append(device_item)
    response_data = json.dumps(did_list)
    return HttpResponse(response_data)



class UploadFileForm(forms.Form):
    file = forms.FileField()

def import_sheet(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)
        def filtrate_dupe(row):
            # row[1] represents device id.
            rd = LabDevice.objects.filter(device_id=row[1]).first()
            if rd == None:  #filter().first() won't return DoesNotExist Error, while get() will.
                return row
            else:
                # return None
                # if rd.lab_location == 'PEK':
                rd.lab_location = row[6]
                rd.owner = row[3]
                rd.label = row[4]
                rd.model = row[0]
                rd.save()


        # if form.is_valid():
        request.FILES.get('file').save_to_database(
            model=LabDevice,
            initializer=filtrate_dupe,
            mapdict=['model', 'device_id', 'os', 'owner', 'label', 'project', 'lab_location', 'status'])
        return HttpResponse("OK")
        # else:
        #     return HttpResponseBadRequest()
    else:
        form = UploadFileForm()
    return render(
        request,
        'motric_upload_form.html',
        {'form': form})


def search(request):
    q = request.GET.copy()
    data = json.dumps(q)
    keyword = q.get('q')
    page = q.get('page')
    searcher = q.get('opt')
    # by = q.get('by') # default by id.

    # strin= shlex.shlex(keyword)
    # strin.whitespace += ":"
    # # strin.whitespace += "|"
    # strin.whitespce_split = True
    # strin.quotes += '|'
    # list_kw = list(strin)

    list_kw = shlex.split(keyword)
    # return HttpResponse(json.dumps(list_kw))

    try:
        query = {}
        for k in list_kw:
            query[k.split(":")[0]] = k.split(":")[1]

        # return HttpResponse(json.dumps(query))

        ## for device search ##
        device_id = query.get('id')
        model = query.get('model')
        project = query.get('project')
        owner = query.get('owner')
        lab_location = query.get('location')
        status = query.get('status')
        label = query.get('label')
        os = query.get('os')
        register_id = query.get('#')

        ## for request search ##
        requester = query.get('requester')
        costcenter = query.get('cost_center')

        status_dict = {'public':'AVA', 'assigned':'ASS', 
        'requested':'REQ', 'approved':'APP', 'refused':'REF',
        'ordered':'ORD', 'received':'REC', 'broken':'BRO',
        'in repair':'REP', 'retrieved':'RET', 'retired':'RTR'}

        result_list = LabDevice.objects.all()
        requestsearch = 0


        if requester:
            ftr = requester.split("|")
            result_list = RequestedDevice.objects.filter(requester__ldap__in=ftr).filter(resolved__in=[0,1]).order_by('-id')
            requestsearch = 1

        if costcenter:
            ftr = costcenter.split("|")
            result_list = RequestedDevice.objects.filter(requester__cost_center__in=ftr)
            requestsearch = 1

        if device_id:
            ftr = device_id.split("|")
            result_list = result_list.filter(device_id__in=ftr)

        if model:
            ftr = model.split("|")
            fltr = reduce(lambda x,y:x|y,  [Q(model__icontains = item) for item in ftr])
            result_list = result_list.filter(fltr)

        if project:
            ftr = project.split("|")
            result_list = dresult_list.filter(project__in=ftr)

        if owner:
            ftr = owner.split("|")
            fltr = reduce(lambda x,y:x|y,  [Q(owner__icontains = item) for item in ftr])
            result_list = result_list.filter(fltr)

        if lab_location:
            ftr = lab_location.split("|")
            result_list = result_list.filter(lab_location__in=ftr)

        if label:
            ftr = label.split("|")
            fltr = reduce(lambda x,y:x|y,  [Q(label__icontains = item) for item in ftr])
            result_list = result_list.filter(fltr)

        if os:
            ftr = os.split("|")
            result_list = result_list.filter(os__in=ftr)

        if status:
            status_list = status.lower().split("|")
            ftr = [ status_dict.get(x) for x in status_list]
            result_list = result_list.filter(status__in=ftr)

        if register_id:
            ftr = register_id.split("|")
            result_list = result_list.filter(id__in=ftr)



    except IndexError:
        return HttpResponse("Please follow the search syntax and try again :)  Click the question mark after the search box for quick help.")

    count = result_list.count()

    paginator = Paginator(result_list, 100) # Show 100 devices per page.
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result_list = paginator.page(paginator.num_pages)

    sh = SearchHistory(query=keyword, searcher=searcher, field=list(query))
    sh.save()
    full_path = request.get_full_path()
    current_path = full_path.split("&")[0]
    if not requestsearch:
        sh.q_type = 1
        sh.save()
        return render(request, 'motric_sr_device.html', {'device_list':result_list, 'count':count, 'first_param':current_path})
    else:
        sh.q_type = 2
        sh.save()
        return render(request, 'motric_sr_request.html', {'request_list':result_list, 'count':count, 'first_param':current_path})
    
    

def malfunction_record(request):
    p = request.POST.copy()
    pk = p.get('pk')
    maltype = p.getlist('maltype')
    ld = LabDevice.objects.get(pk=pk)
    operator = p.get('opt')

    for i in range(len(maltype)):
        mal = MalFunction(device=ld, type=maltype[i])
        mal.save()
        if maltype[i].startswith('1'):
            evt = Event(device=ld, event=log_generator(mal.occur_date, '<span class="noticeable">Broken</span>: ' + mal.get_type_display(), operator))
        if maltype[i].startswith('2'):
            evt = Event(device=ld, event=log_generator(mal.occur_date, '<span class="bold_orange">Malfunction</span>: ' + mal.get_type_display(), operator))
        evt.save()

    return HttpResponse(json.dumps(maltype))

def malfunction_statistics(request):
    mfs = MalFunction.objects.filter(type__gt=200)
    soft_type_lst = [e.get_type_display() for e in mfs]
    soft_counter = Counter(soft_type_lst)
    soft_dct = dict(soft_counter)
    soft_items_tup_lst = sorted(soft_dct.items(), key=lambda pair:pair[1], reverse=True)
    soft_items_lst_lst = [list(e) for e in soft_items_tup_lst]
    soft_sum = mfs.count()
    dct = dict(MalFunction.TYPE)
    new_dct = {v: k for k, v in dct.iteritems()}
    # xlist = []
    for si in soft_items_lst_lst:
        tp = new_dct.get(si[0])
        lds = mfs.filter(type=tp).values_list('device', flat=True).distinct()
        # lds = mfs.filter(type=tp).values('device').distinct()
        # lds = mfs.filter(type=tp).distinct('device')
        lds = [LabDevice.objects.get(pk=e) for e in lds]
        si.append(lds)

    bks = MalFunction.objects.filter(type__lt=200)
    hard_type_lst = [e.get_type_display() for e in bks]
    hard_counter = Counter(hard_type_lst)
    hard_dct = dict(hard_counter)
    hard_items_tup_lst = sorted(hard_dct.items(), key=lambda pair:pair[1], reverse=True)
    hard_items_lst_lst = [list(e) for e in hard_items_tup_lst]
    hard_sum = bks.count()

    for hi in hard_items_lst_lst:
        tp = new_dct.get(hi[0])
        lds = bks.filter(type=tp).values_list('device', flat=True).distinct()
        # lds = bks.filter(type=tp).distinct('device')
        lds = [LabDevice.objects.get(pk=e) for e in lds]
        hi.append(lds)

    return render(request, 'motric_mal_statistics.html', {'soft_mal_list':soft_items_lst_lst, 'hard_mal_list':hard_items_lst_lst, 'soft_sum':soft_sum, 'hard_sum':hard_sum})


def my_request(request):
    request_list = RequestedDevice.objects.filter(assignee=loginer, resolved=0)
    count = request_list.count()
    return render(request, 'motric_pending_request.html', {'request_list': request_list, 'count': count})


def request_dashboard(request):
    import datetime
    from datetime import timedelta
    from decimal import Decimal
    g = request.GET.copy()
    days = g.get('days')
    mode = g.get('standalone')
    # Creating the data
    # rds = RequestedDevice.objects.filter(resolved__in=[0,1])
    rds_valid = RequestedDevice.objects.filter(resolved__in=[0,1]).exclude(request_date__lt=datetime.date(2016, 12, 1)) # We start migrating users from 2016/12
    r_range = timezone.now() - timedelta(days=int(days or 36500)) # 36500 stands for 100 years, enough for query all the requests :D
    rds = rds_valid.filter(request_date__gte=r_range)

    mset = rds.values_list('model_type').annotate(qty=Sum('quantity')).order_by('-qty')
    description_model = [("model_type", "string", "Model"),
                         ("qty", "number", "Quantity")]
    data_model = list(mset)

    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description_model)
    data_table.LoadData(data_model)

    # Create a JavaScript code string, preparing for the table chart.
    jscode_model = data_table.ToJSCode("jscode_data",
                                 columns_order=("model_type", "qty"), order_by="-qty")
    # Create a JSON string, preparing for the pie chart.
    json_model = data_table.ToJSon(columns_order=("model_type", "qty"), order_by="-qty")
    dvc_count = rds.aggregate(total=Sum('quantity'))['total']


    ##### For the column chart, "Count of requests and devices break-down by month".
    if mode == '1':
        rds = rds_valid
    rset = rds.annotate(month=ExtractMonth('request_date'), year=ExtractYear('request_date')).values_list('year', 'month').annotate(request=Count('id'), device=Sum('quantity')).values_list('year', 'month', 'request', 'device')
    r_count = rds.count()
    d_count = rds.aggregate(total=Sum('quantity'))['total']
    data_request_withdev = [(str(e[0]) + "/" + str(e[1]), e[2], e[3]) for e in rset]
    description_request = [("month", "string", "Month"),
                           ("request_times", "number", "# of requests (total: " + str(r_count) + " )"),
                           ("request_device_quantity", "number", "# of devices (total: " + str(d_count) + " )")]

    data_table_r = gviz_api.DataTable(description_request)
    data_table_r.LoadData(data_request_withdev)
    json_request = data_table_r.ToJSon(columns_order=("month", "request_times", "request_device_quantity"))


    ##### For the combo chart, "Response of requests break-down by month".
    fday_overall = []
    for e in rds:
       if e.resolved_date == None:
         fday_overall.append(('OPEN', (timezone.now() - e.request_date).days))
       else:
         fday_overall.append(('RESOLVED', (e.resolved_date - e.request_date).days))

    total = sum(e[1] for e in fday_overall) # the total of the fulfilling days.
    average_overall = Decimal(total, 1)/rds.count()

    rset_nodev = rds.annotate(month=ExtractMonth('request_date'), year=ExtractYear('request_date')).values_list('year', 'month').annotate(request=Count('id')).values_list('year', 'month', 'request')
    data_request_nodev = [(str(e[0]) + "/" + str(e[1]), e[2]) for e in rset_nodev]

    mset_month = rds.datetimes('request_date', 'month')
    data_request_com = []
    x = 0
    for m in mset_month:
       rd_res = rds_valid.filter(resolved_date__year=m.year, resolved_date__month=m.month)  # DONOT set it to rds.
       month_fdays = 0
       for e in rd_res:
         month_fdays += (e.resolved_date - e.request_date).days
       if rd_res.count() == 0:
        continue;
       else:
        month_average = round(Decimal(month_fdays, 1)/rd_res.count(), 1)
       # print m, month_fdays, rd_res.count(), month_average
       data_request_com.append(data_request_nodev[x] + (rd_res.count(), month_average))
       x += 1


    resolved_count = rds.filter(resolved=1).count()
    description_resolved_r = [("month", "string", "Month"),
                              ("request_amount", "number", "# of submitted requests (total: " + str(r_count) + " )"),
                              ("resolved_request_amount", "number", "# of resolved requests (total: " + str(resolved_count) + " )"),
                              ("month_res_average", "number", "Average fulfilling days")]

    data_table_resolved_r =  gviz_api.DataTable(description_resolved_r)
    data_table_resolved_r.LoadData(data_request_com)
    json_resolved_r = data_table_resolved_r.ToJSon(columns_order=("month", "request_amount", "resolved_request_amount", "month_res_average"))


    ##### For the table chart "Response of requests break-down by month".
    data_request_com_4tc = []
    accum_rts = 0
    accum_res = 0
    for e in data_request_com:
       accum_rts += e[1]
       accum_res += e[2]
       res_ratio = round(Decimal(accum_res, 1)/accum_rts, 2)
       print "{0:.0f}%".format(res_ratio * 100)
       data_request_com_4tc.append(e + (accum_rts, accum_res, str(res_ratio * 100) + '%'))

    description_resolved_4tc = [("month", "string", "Month"),
                              ("request_amount", "number", "submitted requests"),
                              ("resolved_request_amount", "number", "resolved requests"),
                              ("month_res_average", "number", "average fulfilling days"),
                              ("accum_rts", "number", "accumulation of submitted"),
                              ("accum_res", "number", "accumulation of resolved"),
                              ("resolve ratio", "string", "resolve ratio"),
                              ]

    data_table_resolved_4tc = gviz_api.DataTable(description_resolved_4tc)
    data_table_resolved_4tc.LoadData(data_request_com_4tc)
    json_resolved_4tc = data_table_resolved_4tc.ToJSon(columns_order=("month", "request_amount", "resolved_request_amount", "month_res_average", 
                                                                   "accum_rts", "accum_res", "resolve ratio"),)


    #### For the pie charts "Requests breakdown by lab location"
    cnt_labloc = Counter(list(rds.values_list('lab_location')));
    data_labloc = [k + (v,) for k,v in cnt_labloc.items()];
    description_labloc = [("lab_location", "string", "Lab location"),
                        ("request_count", "number", "Requests on each location"),
                        ]

    data_table_labloc = gviz_api.DataTable(description_labloc)
    data_table_labloc.LoadData(data_labloc)
    json_labloc = data_table_labloc.ToJSon(columns_order=("lab_location", "request_count"), order_by="-request_count")


    cnt_preflab = Counter(list(rds.values_list('requester__pref_location')));
    data_preflab = [k + (v,) for k,v in cnt_preflab.items()];
    # import unicodedata
    # data_preflab = [tuple(map(lambda i: str.replace(unicodedata.normalize('NFKD', i).encode('ascii','ignore'), '', 'Whatever'), tup)) for tup in data_preflab]
    data_preflab = [tuple('No Preference' if x == '' else x for x in tup) for tup in data_preflab]


    description_preflab = [("pref_location", "string", "Preferred location"),
                         ("request_count", "number", "Preferred location for the requests"),
                         ]

    data_table_preflab = gviz_api.DataTable(description_preflab)
    data_table_preflab.LoadData(data_preflab)
    json_preflab = data_table_preflab.ToJSon(columns_order=("pref_location", "request_count"), order_by="-request_count")


    #### For the column chart "Location distribution break-down by month upon request"
    data_request_loc_cc = []
    data_month = [(str(e[0]) + "/" + str(e[1])) for e in rset_nodev]
    i = 0
    for m in mset_month:
       rd_res = rds.filter(request_date__year=m.year, request_date__month=m.month)
       vl = rd_res.values_list('lab_location', 'requester__pref_location')
       ct_lab = Counter(e[0] for e in vl)
       ct_pref = Counter(e[1] for e in vl)
       # each_month = [data_month[i], dict(ct_lab), dict(ct_pref)] # use this can get the readable data for each location.
       # each_month = (data_month[i],) + (ct_lab.values(),) + (ct_pref.values(),)
       # each_month = (data_month[i],) + tuple(ct_lab.values()) + tuple(ct_pref.values()) ## This is not controlable if the values are not fixed.
       each_month = (data_month[i],) + (ct_lab['MTV'], ct_lab['PEK'], ct_lab['TWD']) + (ct_pref[''], ct_pref['MTV'], ct_pref['PEK'], ct_pref['TWD'])
       data_request_loc_cc.append(each_month)
       i += 1

    description_loc_trends = [("month", "string", "Month"),
                            ("count_mtv","number", "Located on MTV (" + str(cnt_labloc[('MTV',)]) + ")"), ("count_pek", "number", "Located on PEK (" + str(cnt_labloc[('PEK',)]) + ")"), ("count_twd", "number", "Located on TWD (" + str(cnt_labloc[('TWD',)]) + ")"),
                            ("pre_ct_dontcare", "number", "No Preferrence (" + str(cnt_preflab[('',)]) + ")"), ("pre_ct_mtv", "number", "Preferred on MTV (" + str(cnt_preflab[('MTV',)]) + ")"), ("pre_ct_pek","number", "Preferred on PEK (" + str(cnt_preflab[('PEK',)]) + ")"), ("pre_ct_twd","number", "Preferred on TWD (" + str(cnt_preflab[('TWD',)]) + ")")     
                            ]
    data_table_loc_trends_cc = gviz_api.DataTable(description_loc_trends)
    data_table_loc_trends_cc.LoadData(data_request_loc_cc)
    json_loc_trends = data_table_loc_trends_cc.ToJSon(columns_order=("month", "count_mtv", "count_pek", "count_twd", "pre_ct_dontcare", "pre_ct_mtv", "pre_ct_pek", "pre_ct_twd"))



    #### For the pie charts "Devices break-down by lab location"
    data_device_loc = rds.values_list('lab_location').annotate(device=Sum('quantity')).values_list('lab_location', 'device')
    description_device_loc = [("lab_location", "string", "Lab location"),
                        ("device_count", "number", "Devices on each location"),
                        ]
    data_table_device_loc = gviz_api.DataTable(description_device_loc)
    data_table_device_loc.LoadData(data_device_loc)
    json_device_loc = data_table_device_loc.ToJSon(columns_order=("lab_location", "device_count"), order_by="-device_count")


    data_device_pref_loc_set = rds.values_list('requester__pref_location').annotate(device=Sum('quantity')).values_list('requester__pref_location', 'device')
    data_device_pref_loc = [tuple('No Preference' if x == '' else x for x in tup) for tup in data_device_pref_loc_set]
    description_device_pref_loc = [("pref_location", "string", "Preferred location"),
                        ("device_count", "number", "Prefered location for the devices"),
                        ]
    data_table_device_pref_loc = gviz_api.DataTable(description_device_pref_loc)
    data_table_device_pref_loc.LoadData(data_device_pref_loc)
    json_device_pref_loc = data_table_device_pref_loc.ToJSon(columns_order=("pref_location", "device_count"), order_by="-device_count")


    #### For the column charts "Location distribution break-down by month upon device"
    data_device_loc_cc = []
    i = 0
    mset_month = rds.datetimes('request_date', 'month')
    for m in mset_month:
        rd_res = rds.filter(request_date__year=m.year, request_date__month=m.month)
        labloc = rd_res.values_list('lab_location').annotate(device=Sum('quantity')).values_list('lab_location', 'device').order_by('lab_location')
        prefloc = rd_res.values_list('requester__pref_location').annotate(device=Sum('quantity')).values_list('requester__pref_location', 'device').order_by('requester__pref_location')
        # each_month = (data_month[i],) + tuple([e[1] for e in labloc]) + tuple([e[1] for e in prefloc])
        dict_labloc = dict(labloc)
        dict_prefloc = dict(prefloc)
        each_month = (data_month[i],) + (dict_labloc.get('MTV'), dict_labloc.get('PEK'), dict_labloc.get('TWD'),) + (dict_prefloc.get(''), dict_prefloc.get('MTV'), dict_prefloc.get('PEK'), dict_prefloc.get('TWD')) ### Like above, this seems clumsy but in fact more stable.
        data_device_loc_cc.append(each_month)
        i += 1

    description_loc_device_trends = [("month", "string", "Month"),
                            # ("count_mtv","number", "Located on MTV (" + str(data_device_loc.order_by('lab_location')[0][1]) + ")"), ("count_pek", "number", "Located on PEK (" + str(data_device_loc.order_by('lab_location')[1][1]) + ")"),
                            ("count_mtv","number", "Located on MTV (" + str(dict(data_device_loc)['MTV']) + ")"), ("count_pek", "number", "Located on PEK (" + str(dict(data_device_loc)['PEK']) + ")"), ("count_twd","number", "Located on TWD (" + str(dict(data_device_loc)['TWD']) + ")"),
                            # ("pre_ct_dontcare", "number", "No Preferrence (" + str(data_device_pref_loc_set.order_by('requester__pref_location')[0][1]) + ")"), ("pre_ct_mtv", "number", "Preferred on MTV (" + str(data_device_pref_loc_set.order_by('requester__pref_location')[1][1]) + ")"), ("pre_ct_pek","number", "Preferred on PEK (" + str(data_device_pref_loc_set.order_by('requester__pref_location')[2][1]) + ")"), ("pre_ct_twd","number", "Preferred on TWD (" + str(data_device_pref_loc_set.order_by('requester__pref_location')[3][1]) + ")"), 
                            ("pre_ct_dontcare", "number", "No Preferrence (" + str(dict(data_device_pref_loc_set)['']) + ")"), ("pre_ct_mtv", "number", "Preferred on MTV (" + str(dict(data_device_pref_loc_set)['MTV']) + ")"), ("pre_ct_pek","number", "Preferred on PEK (" + str(dict(data_device_pref_loc_set)['PEK']) + ")"), ("pre_ct_twd","number", "Preferred on TWD (" + str(dict(data_device_pref_loc_set)['TWD']) + ")"), 
                            ]

    data_table_loc_device_trends_cc = gviz_api.DataTable(description_loc_device_trends)
    data_table_loc_device_trends_cc.LoadData(data_device_loc_cc)
    json_loc_device_trends = data_table_loc_device_trends_cc.ToJSon(columns_order=("month", "count_mtv", "count_pek", "pre_ct_dontcare", "pre_ct_mtv", "pre_ct_pek", "pre_ct_twd"),)

    return render(request, 'motric_request_statistics.html', 
        {'jscode':jscode_model, 'json_model':json_model, 
        'json_request':json_request, 'r_count':r_count, 'd_count':dvc_count, 
        'json_resolved':json_resolved_r, 'json_resolved_4tc':json_resolved_4tc, 
        'json_labloc':json_labloc, 'json_preflab':json_preflab, 'json_loc_trends':json_loc_trends,
        'json_device_loc':json_device_loc, 'json_device_pref_loc':json_device_pref_loc, 'json_loc_device_trends':json_loc_device_trends })