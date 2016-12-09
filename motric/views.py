from django.shortcuts import render
from django.http import HttpResponse
from models import *

# Create your views here.
def index(request):
	return render(request, 'motric_nav.html')
	# return HttpResponse("Hello World, I'm a Django sample app named Polls, you're now at the Polls index.")

def home(request):
	device_list = LabDevice.objects.filter(status__in=['AVA', 'ASS']).order_by('-id')
	return render(request, 'motric_home.html', {'device_list':device_list})

def public_device(request):
	device_list = LabDevice.objects.filter(status='AVA').order_by('-id')
	return render(request, 'motric_public.html', {'device_list':device_list})

def dedicated_device(request):
	device_list = LabDevice.objects.filter(status='ASS').order_by('-id')
	return render(request, 'motric_dedicated.html', {'device_list':device_list})

def broken_device(request):
	device_list = LabDevice.objects.filter(status='BRO').order_by('-id')
	return render(request, 'motric_broken.html', {'device_list':device_list})

def device_request(request):
	return render(request, 'motric_request.html')

def request_disposal(request):
	request_list = RequestedDevice.objects.filter(status__in=['REQ', 'APP', 'ORD', 'REC']).order_by('-id') # return a list with the lastest request shown first.
	return render(request, 'motric_disposal.html', {'request_list':request_list})

# def faq(request):
# 	return render(request, 'motric_faq.html')

# def about(request):
# 	return render(request, 'motric_about.html')

# This is an incorrect configuration.
# def receiver(request):
# 	return render(request, 'receiver.jsonReceiver')
# --------------------------------------------------

# Below works, but basically this is not a good way to response the request in views.py. 
# We need to separate the logic part to a separated python file to tackle the the request.

# def receiver(request):

#     # dict = {}
#     # try:
#     # 	# dict['HttpRequest.path']=request.path
#     # 	# dict['HttpRequest.method']=request.method
#     # 	# dict['HttpRequest.body']=request.body
#     # 	dict['HttpRequest.POST']=request.POST

#     # except:
#     #     import sys
#     #     info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
#     #     dict['message'] = info
#     #     dict['create_at'] = str(time.ctime())
    
#     # response = json.dumps(dict)
#     # data = request.POST
#     # return HttpResponse(type(data))

# 	response = HttpResponse()
# 	response.write("<p><h2>I received json data as following:</h2></p>")
# 	response.write("<p>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~</p>")
# 	response.write(json.dumps(request.POST))
# 	response.write("<p>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~</p>")
# 	response.write("<p><h3>I'll parse them and put them into database later.<h3/></p>")
# 	return HttpResponse(response.content)
#     # return HttpResponse(json.dumps(request.POST))