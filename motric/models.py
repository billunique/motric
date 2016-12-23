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
		('REP', 'In repair'),
		('RET', 'Retired (Recycled)'),
	)
	status = models.CharField(max_length=3, choices=STATUS)

	class Meta:
		abstract = True

class Requester(models.Model):
	ldap = models.CharField(max_length=30)
	cost_center = models.CharField(max_length=50)
	project = models.CharField(max_length=50)
	device_owner = models.CharField(max_length=100)
	device_label = models.CharField(max_length=50)
	pref_location = models.CharField(max_length=3)

	def __unicode__(self):
		return u'%s, from project %s' % (self.ldap, self.project)

class RequestedDevice(DeviceStatus):
	model_type = models.CharField(max_length=30)
	quantity = models.IntegerField(default=1)
	os_version = models.CharField(max_length=50)
	requester = models.ForeignKey(Requester, on_delete=models.CASCADE)
	request_date = models.DateTimeField(auto_now_add=True) 
	approve_date = models.DateTimeField(blank=True, null=True, editable=False)
	lab_location = models.CharField(max_length=3, blank=True, null=True)
	po_number = models.CharField(max_length=50, blank=True, null=True)
	po_date = models.DateTimeField(blank=True, null=True)
	price_usd = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
	price_cny = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
	ex_rate = models.FloatField(blank=True, null=True)
	receive_date = models.DateTimeField(blank=True, null=True)
	resolved = models.BooleanField(default=False)
	resolved_date = models.DateTimeField(blank=True, null=True)
	comment = models.CharField(max_length=128)

	def __unicode__(self):
		return u'%s %s, with %s, requested by %s, for %s project' % (self.quantity, self.model_type, self.os_version, self.requester.ldap, self.requester.project)
		# return self.model_type

class LabDevice(DeviceStatus):
	# model = models.OneToOneField(RequestedDevice)  # OneToOne is smilar to ForeignKey but unique=true, this is not the case.
	# model = models.ForeignKey(RequestedDevice)
	model = models.CharField(max_length=30)
	# respond_to = models.ManyToManyField(RequestedDevice)  # Many labdevices could respond to one requesteddevice; meanwhile many requesteddevice could be responded by one labdevice (such as firstly public then assigned, or as result of device replacement.)
	respond_to = models.ManyToManyField(RequestedDevice, through='ResponseRelationship') 
	device_id = models.CharField(max_length=100)
	register_date = models.DateTimeField('date device_id recorded', auto_now_add=True) # The register date is basically fixed. While other status could be mutable. 
	os = models.CharField(max_length=50, blank=True)
	owner = models.CharField(max_length=100, blank=True)
	user = models.CharField(max_length=100, blank=True)  # Those who have the device usage access.
	label = models.CharField(max_length=50, blank=True)
	project = models.CharField(max_length=50, blank=True)
	replaced_by = models.ManyToManyField('self', symmetrical=False)

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
