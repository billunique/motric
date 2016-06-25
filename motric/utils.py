from django.http import HttpResponse, HttpRequest, QueryDict
from django.core.mail import send_mail
from django.utils import timezone
from models import RequestedDevice, Requester
import time, json


def form_receiver(request):

    form_dict = request.POST.copy() # Interesting! This is naturally a dictionary (QueryDict), can be used for parse directly.
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
        import sys
        dict = {}
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        dict['message'] = info
        dict['create_at'] = str(time.ctime())

    message = ldap + ' raised device request for:\n\n' + combo + '\n\nGo to http://motric.bej.corp.google.com/request_disposal for details.'
    send_mail(
        '[Motric]Somebody raised device request!',
        message,
        'mobileharness.motric@gmail.com',
        ['xiawang@google.com', 'yanyanl@google.com'],
        fail_silently=False
    )

    return HttpResponse("Thanks for using Mobile Harness! We've received your request, if it's approved, we'll start purchasing shortly. Please stay tuned.")


    # response = HttpResponse()
    # response.write("<p><h2>I received json data as following:</h2></p>")
    # response.write("<p>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~</p>")
    # form_content = json.dumps(request.POST)
    # response.write(type(form_content).str())
    # response.write("<p>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~</p>")
    # response.write("<p><h3>I'll parse them and put them into database later, wahahahaha.<h3/></p>")
    # return HttpResponse(response.content)


    # if request.method == 'POST':
    #     json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
    #     try:
    #       data = json_data['data']
    #     except KeyError:
    #       HttpResponseServerError("Malformed data!")
    #     HttpResponse("Got json data")
