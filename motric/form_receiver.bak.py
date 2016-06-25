from django.http import HttpResponse
import time
import json

def jsonReceiver(request):

    # dict = {}
    # try:
    # 	# dict['HttpRequest.path']=request.path
    # 	# dict['HttpRequest.method']=request.method
    # 	# dict['HttpRequest.body']=request.body
    # 	dict['HttpRequest.POST']=request.POST

    # except:
    #     import sys
    #     info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    #     dict['message'] = info
    #     dict['create_at'] = str(time.ctime())
    
    # response = json.dumps(dict)
    # data = request.POST
    # return HttpResponse(type(data))

	response = HttpResponse()
	response.write("<p><h2>I received json data as following:</h2></p>")
	response.write("<p>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~</p>")
	response.write(json.dumps(request.POST))
	response.write("<p>~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~</p>")
	response.write("<p><h3>I'll parse them and put them into database later, wahahahaha.<h3/></p>")
	return HttpResponse(response.content)
    # return HttpResponse(json.dumps(request.POST))