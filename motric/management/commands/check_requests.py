from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail, EmailMessage
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from motric.models import RequestedDevice, LabDevices
from motric.utils import EmailThread, motric_send_mail
import socket


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('dd', nargs='+', type=int, help='an integer for the days duration.')

        # Named (optional) arguments

    def handle(self, *args, **options):
    	# print 'args = ', args
    	# print 'options = ', options

    	motric_host = "motric"
        subject = '[Motric]Requests that need your attention!'
        sender = 'mobileharness.motric@gmail.com'
        recipient = ['mobileharness-ops@google.com', 'mobileharness-ops-mtv@google.com']
        cc_rcpt = []

        if 'motric' not in socket.gethostname():
            motric_host = "xiawang.bej:8080"
            recipient = ['xiawang@google.com']

    	rds = RequestedDevice.objects.all()
    	days_warn = options['dd'][0]
    	days_danger = options['dd'][1]
    	time_width_w = timezone.now() - timedelta(days=days_warn)
    	time_width_d = timezone.now() - timedelta(days=days_danger)
    	warn_set = rds.filter(request_date__lt=time_width_w, request_date__gt=time_width_d).filter(resolved=0)
    	danger_set = rds.filter(request_date__lte=time_width_d).filter(resolved=0)
    	table_w = '<table cellpadding="3" border="1" style="border:2px solid gray; border-collapse:collapse"><caption style="color:orange; font-size:14px; font-weight:bold; text-align:left; margin-bottom:5px">Requests that not fulfilled for more than ' + str(days_warn) + ' days but less than ' + str(days_danger) + ' days (count: ' + str(warn_set.count()) + ')</caption><tr><th>Summary</th><th>Location</th><th>Assignee</th><th>Link</th></tr>'
    	for e in warn_set:
    		table_w += '<tr><td>' + str(e) + '</td><td>' + e.lab_location + '</td><td>' + str(e.assignee or "") + '</td><td>https://' + motric_host + '/details/?t=r&pk=' + str(e.id) + '</td></tr>'
    	table_w += '</table>'

    	table_d = '<table cellpadding="3" border="1" style="border:2px solid gray; border-collapse:collapse"><caption style="color:red; font-size:14px; font-weight:bold; text-align:left; margin-bottom:5px">Requests that not fulfilled for more than ' + str(days_danger) + ' days (count: ' + str(danger_set.count()) + ')</caption><tr><th>Summary</th><th>Location</th><th>Assignee</th><th>Link</th></tr>'
    	for e in danger_set:
    		table_d += '<tr><td>' + str(e) + '</td><td>' + e.lab_location + '</td><td>' + str(e.assignee or "") + '</td><td>https://' + motric_host + '/details/?t=r&pk=' + str(e.id) + '</td></tr>'
    	table_d += '</table>'

    	message = 'Hi <b><span style="color:#4285F4">t</span><span style="color:#EA4335">e</span><span style="color:#FBBC05">a</span><span style="color:#34A853">m</span></b>,<br/><br/>Please check following requests and try to fulfill them asap.<br/><br/>' + table_d + '<p></p>' + table_w

    	motric_send_mail(
    	    subject,
    	    message,
    	    sender,
    	    recipient, 
    	    cc_rcpt
    	)

        lds_exclusive = LabDevices.objects.filter(exclusive=1)
        time_threshold = timezone.now() - relativedelta(years=2) 