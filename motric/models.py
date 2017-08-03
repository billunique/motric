from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField

# Create your models here.

class DeviceStatus(models.Model):
	STATUS = (
		('REQ', 'Requested'), 
		('APP', 'Approved'),
		('REF', 'Refused'),
		('ORD', 'Ordered'), # When PO number is added.
		('REC', 'Received'), # When device received but before registered.
		('REG', 'Registered'), # When device id is added.
		('AVA', 'Public'), # When device is brought online.
		('ASS', 'Assigned'), # When device is allocated to specific user.
		('WIT', 'Withdrawn'), # When device is brought offline intendedly.
		('BRO', 'Broken'),
		('REP', 'In Repair'),
		('RET', 'Retrieved'), # When device is successfully recovered and brought back.
		('RTR', 'Retired'), # When device is totally withdrawn and recycled.
	)
	status = models.CharField(max_length=3, choices=STATUS)

	class Meta:
		abstract = True

class Requester(models.Model):
	ldap = models.CharField(max_length=100)
	cost_center = models.CharField(max_length=50)
	project = models.CharField(max_length=50)
	device_owner = models.CharField(max_length=100)
	device_label = models.CharField(max_length=50, blank=True, null=True)
	pref_location = models.CharField(max_length=3, blank=True, null=True)

	def __unicode__(self):
		return u'%s, from project %s' % (self.ldap, self.project)

class RequestedDevice(DeviceStatus):
	model_type = models.CharField(max_length=30)
	quantity = models.IntegerField(default=1)
	os_version = models.CharField(max_length=50, blank=True, null=True)
	requester = models.ForeignKey(Requester, on_delete=models.CASCADE)
	request_date = models.DateTimeField(auto_now_add=True)
	approve_date = models.DateTimeField(blank=True, null=True, editable=False)
	lab_location = models.CharField(default='PEK', max_length=3, blank=True, null=True)
	po_number = models.CharField(max_length=50, blank=True, null=True)
	po_date = models.DateTimeField(blank=True, null=True)
	price_usd = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
	price_cny = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
	ex_rate = models.FloatField(blank=True, null=True)
	receive_date = models.DateTimeField(blank=True, null=True)
	resolved = models.BooleanField(default=False)
	resolved_date = models.DateTimeField(blank=True, null=True)
	comment = models.CharField(max_length=256, blank=True, null=True)
	charged = models.BooleanField(default=False)
	bug_id = models.CharField(max_length=100, blank=True, null=True)
	eta_date = models.DateTimeField(blank=True, null=True)
	assignee = models.CharField(max_length=100, blank=True, null=True)

	def __unicode__(self):
		return u'%s %s, requested by %s, for %s project' % (self.quantity, self.model_type, self.requester.ldap, self.requester.project)
		# return self.model_type

class LabDevice(DeviceStatus):
	# model = models.OneToOneField(RequestedDevice)  # OneToOne is smilar to ForeignKey but unique=true, this is not the case.
	# model = models.ForeignKey(RequestedDevice)
	model = models.CharField(max_length=100)
	# respond_to = models.ManyToManyField(RequestedDevice)  # Many labdevices could respond to one requesteddevice; meanwhile many requesteddevice could be responded by one labdevice (such as firstly public then assigned, or as result of device replacement.)
	respond_to = models.ManyToManyField(RequestedDevice, through='ResponseRelationship') 
	device_id = models.CharField(max_length=100, unique=True)
	register_date = models.DateTimeField('date device_id recorded', auto_now_add=True) # The register date is basically fixed. While other status could be mutable. 
	os = models.CharField(max_length=50, blank=True, null=True)
	owner = models.CharField(max_length=5120, blank=True, null=True)
	user = models.CharField(max_length=100, blank=True, null=True)  # Those who have the device usage access.
	label = models.CharField(max_length=50, blank=True, null=True)
	project = models.CharField(max_length=50, blank=True, null=True)
	lab_location = models.CharField(max_length=3, blank=True, null=True)
	price_usd = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
	price_cny = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
	po_number = models.CharField(max_length=50, blank=True, null=True)
	po_date = models.DateTimeField(blank=True, null=True)
	broken_date = models.DateTimeField(blank=True, null=True)
	replaced_by = models.ManyToManyField('self', symmetrical=False, blank=True)
	replaced = models.BooleanField(default=False)

	def __unicode__(self):
		return u'%s, %s, with os %s, for project %s' % (self.model, self.device_id, self.os, self.project)

class ResponseRelationship(models.Model):
	device = models.ForeignKey(LabDevice, on_delete=models.CASCADE)
	request = models.ForeignKey(RequestedDevice, on_delete=models.CASCADE)
	response_date = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u'%s ***** %s, reponsed at %s' % (self.device, self.request, self.response_date)

class Event(models.Model):
	event_id = models.AutoField(primary_key=True)
	device = models.ForeignKey(LabDevice, on_delete=models.CASCADE, blank=True, null=True)
	request = models.ForeignKey(RequestedDevice, on_delete=models.CASCADE, blank=True, null=True)
	# event = models.CharField(max_length=512) # used to store all the events expressed in JSON.
	event = JSONField() # used to store all the events expressed in JSON.

	def __unicode__(self):
		return u'%s, %s' % (self.event_id, self.event)

class MalFunction(models.Model):
	device = models.ForeignKey(LabDevice, on_delete=models.CASCADE, blank=True, null=True)
	TYPE = (
		('101', 'Cannot power on'), 
		('102', 'Screen cannot go light'),
		('103', 'Screen touch broken'),
		('104', 'Scramble screen'),
		('105', 'Wifi hardware broken'),
		('106', 'SDcard broken'),
		('107', 'Battery broken'),
		('108', 'Screen fragmentation'),
		('201', 'Disconnected(usb)'),
		('202', 'Offline(usb)'),
		('203', 'Unauthorized(usb)'),
		('204', 'Lose internet connection'),
		('205', 'Stuck on fastboot screen'),
		('206', 'Stuck on splash screen'),
		('207', 'Stuck on white screen'),
		('208', 'Reboot loop'),
		('209', 'Not able to be reset'),
		('1001', 'Others'),
	)
	type = models.CharField(max_length=4, choices=TYPE)
	occur_date = models.DateTimeField(auto_now_add=True)
	fix_date = models.DateTimeField(blank=True, null=True)

	def __unicode__(self):
		return u'%s, %s, %s' % (self.type, self.occur_date, self.device)


class Usage(models.Model):
	request = models.ForeignKey(RequestedDevice, on_delete=models.CASCADE, blank=True, null=True)
	USAGE = (
		('FT', 'Functionality Test'), 
		('SHT', 'System Health(battery, memory, latency) Test'),
		('ST', 'Stablity Test'),
		('NTU', 'Non-testing Usage'),
		('OTR', 'Others'),
	)
	used_for = models.CharField(max_length=3, choices=USAGE)
	others_detail = models.CharField(max_length=200, blank=True, null=True)

	def __unicode__(self):
		return u'%s; %s' % (self.request, self.used_for)


class SearchHistory(models.Model):
	query = models.CharField(max_length=1000, blank=True, null=True)
	q_type = models.IntegerField(blank=True, null=True)
	field = models.CharField(max_length=100, blank=True, null=True)
	searcher = models.CharField(max_length=50, blank=True, null=True)
	q_date = models.DateTimeField(auto_now_add=True)