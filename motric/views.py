from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import datetime
from models import *

# Create your views here.
def index(request):
	return render(request, 'motric_nav.html')

def home(request):
	return render(request, 'motric_home.html')

def labdevice(request):
	device_list_all = LabDevice.objects.filter(status__in=['AVA', 'ASS']).order_by('-id')
	q = request.GET.copy()
	loc = q.get('loc')
	page = q.get('page')

	device_list = device_list_all
	if loc:
		if loc == 'pek':
			device_list = device_list_all.filter(lab_location='PEK')
		if loc == 'mtv':
			device_list = device_list_all.filter(lab_location='MTV')
		if loc == 'twd':
			device_list = device_list_all.filter(lab_location='TWD')

	count = device_list.count()
	paginator = Paginator(device_list, 100) # Show 100 devices per page.
	try:
	    device_list = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    device_list = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    device_list = paginator.page(paginator.num_pages)
	return render(request, 'motric_labdevice.html', {'device_list':device_list, 'count':count})

def public_device(request):
	device_list_all = LabDevice.objects.filter(status='AVA').order_by('-id')
	q = request.GET.copy()
	loc = q.get('loc')
	page = q.get('page')

	device_list = device_list_all
	if loc:
		if loc == 'pek':
			device_list = device_list_all.filter(lab_location='PEK')
		if loc == 'mtv':
			device_list = device_list_all.filter(lab_location='MTV')
		if loc == 'twd':
			device_list = device_list_all.filter(lab_location='TWD')
	count = device_list.count()
	paginator = Paginator(device_list, 100) # Show 100 devices per page.
	try:
	    device_list = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    device_list = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    device_list = paginator.page(paginator.num_pages)
	return render(request, 'motric_public.html', {'device_list':device_list, 'count':count})

def dedicated_device(request):
	device_list_all = LabDevice.objects.filter(status='ASS').order_by('-id')
	q = request.GET.copy()
	loc = q.get('loc')
	page = q.get('page')

	device_list = device_list_all
	if loc:
		if loc == 'pek':
			device_list = device_list_all.filter(lab_location='PEK')
		if loc == 'mtv':
			device_list = device_list_all.filter(lab_location='MTV')
		if loc == 'twd':
			device_list = device_list_all.filter(lab_location='TWD')
	count = device_list.count()
	paginator = Paginator(device_list, 100) # Show 100 devices per page.
	try:
	    device_list = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    device_list = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    device_list = paginator.page(paginator.num_pages)
	return render(request, 'motric_dedicated.html', {'device_list':device_list, 'count':count})

def broken_device(request):
	device_list_all = LabDevice.objects.filter(status__in=['BRO', 'REP', 'RET', 'RTR']).order_by('-id')
	q = request.GET.copy()
	loc = q.get('loc')
	page = q.get('page')

	device_list = device_list_all
	if loc:
		if loc == 'pek':
			device_list = device_list_all.filter(lab_location='PEK')
		if loc == 'mtv':
			device_list = device_list_all.filter(lab_location='MTV')
		if loc == 'twd':
			device_list = device_list_all.filter(lab_location='TWD')
	count = device_list.count()
	paginator = Paginator(device_list, 100) # Show 100 devices per page.
	try:
	    device_list = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
	    device_list = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
	    device_list = paginator.page(paginator.num_pages)
	return render(request, 'motric_broken.html', {'device_list':device_list, 'count':count})

def device_request(request):
	return render(request, 'motric_request.html')

def request_disposal(request):
	# request_list = RequestedDevice.objects.filter(status__in=['REQ', 'APP', 'ORD', 'REC']).order_by('-id') # return a list with the lastest request shown first.
	request_list = RequestedDevice.objects.filter(resolved=0).order_by('-id') # return a list with the lastest request shown first.
	q = request.GET.copy()
	# f = q['f'] // bad method, in this way the f parameter is mandatory. 
	s = q.get('s')
	l = q.get('l')
	if s:
		if s == 'req':
			request_list = request_list.filter(status='REQ')
		if s == 'app':
			request_list = request_list.filter(status='APP')
		if s == 'ord':
			request_list = request_list.filter(status='ORD')
		if s == 'rec':
			request_list = request_list.filter(status='REC')
		if s == 'all':
			pass
	if l:
		if l == 'pek':
			request_list = request_list.filter(lab_location='PEK')
		if l == 'mtv':
			request_list = request_list.filter(lab_location='MTV')
		if l == 'twd':
			request_list = request_list.filter(lab_location='TWD')
		if l == 'all':
			pass

	count = request_list.count()
	return render(request, 'motric_pending_request.html', {'request_list':request_list, 'count':count})

def request_history(request):
	# request_list = RequestedDevice.objects.filter(status__in=['ASS', 'AVA', 'REF']).order_by('-id') # return a list with the lastest request shown first.
	request_list = RequestedDevice.objects.filter(resolved=1).order_by('-id') # return a list with the lastest request shown first.
	q = request.GET.copy()
	# f = q['f']
	s = q.get('s')
	l = q.get('l')
	ao = q.get('ao')
	if ao:
		today = datetime.date.today()
		this_month = today.month
		last_month = 1
		if this_month == 1:
			last_month = 12
		else:
			last_month = this_month -1
		if ao == 'tm':
			# request_list = RequestedDevice.objects.filter(request_date__month=this_month, resolved=1).order_by('-id')
			request_list = request_list.filter(request_date__month=this_month)
		if ao == 'lm':
			# request_list = RequestedDevice.objects.filter(request_date__month=last_month, resolved=1).order_by('-id')
			request_list = request_list.filter(request_date__month=last_month)
		if ao == 'more':
			# request_list = RequestedDevice.objects.filter(request_date__date__lt=datetime.date(today.year, last_month, 1)).order_by('-id')
			# request_list = RequestedDevice.objects.filter(resolved=1).exclude(request_date__month__in=[this_month, last_month]).order_by('-id')
			request_list = request_list.exclude(request_date__month__in=[this_month, last_month])
	if s:
		if s == 'ass_uc':
			request_list = request_list.filter(status='ASS', charged='0')
		if s == 'ass':
			request_list = request_list.filter(status='ASS')
		if s == 'pub':
			request_list = request_list.filter(status='AVA')
		if s == 'ref':
			request_list = request_list.filter(status='REF')
		if s == 'all':
			pass
	if l:
		if l == 'pek':
			request_list = request_list.filter(lab_location='PEK')
		if l == 'mtv':
			request_list = request_list.filter(lab_location='MTV')
		if l == 'twd':
			request_list = request_list.filter(lab_location='TWD')
		if l == 'all':
			pass

	count = request_list.count()
	return render(request, 'motric_resolved_request.html', {'request_list':request_list, 'count':count})

def device_register(request):
	return render(request, 'motric_register.html')

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