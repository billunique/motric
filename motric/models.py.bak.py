from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Requester(models.Model):
	ldap = models.CharField(max_length=30)
	cost_center = models.CharField(max_length=30)
	project = models.CharField(max_length=50)
	device_owner = models.CharField(max_length=100)
	device_label = models.CharField(max_length=30)

	def __unicode__(self):
		return self.ldap

class RequestedDevice(models.Model):
	model_type = models.CharField(max_length=30)
	quantity = models.IntegerField(default=1)
	os_version = models.CharField(max_length=50)
	request_date = models.DateTimeField('date request submitted', auto_now_add=True) 
	approve_date = models.DateTimeField('date request approved', blank=True, null=True)
	po_date = models.DateTimeField('date purchase started', blank=True, null=True)
	po_number = models.CharField(max_length=15, blank=True)
	price_usd = models.CharField(max_length=15, blank=True)
	price_cny = models.CharField(max_length=15, blank=True)
	requester = models.ForeignKey(Requester, on_delete=models.CASCADE)
	REQUEST_STATUS = (
		('REQ', 'Requested'), 
		('APP', 'Approved'),
		('REF', 'Refused'),
		('ORD', 'Ordered'), # When PO number is added.
		('REC', 'Received'), # When device received but before registered.
	)
	request_status = models.CharField(max_length=3, choices=REQUEST_STATUS)

	def __unicode__(self):
		return u'%s, with os %s, requested by %s, for %s project' % (self.model_type, self.os_version, self.requester.ldap, self.requester.project)
		# return self.model_type

class LabDevice(models.Model):
	model = models.OneToOneField(RequestedDevice)
	device_sn = models.CharField(max_length=100)
	STATUS = (
		('REG', 'Registered'), # When device id is added.
		('AVA', 'Available (Public)'), # When device is brought online.
		('ASS', 'Assigned'), # When device is allocated to specific user.
		('WIT', 'Withdrawed'), # When device is brought offline intendedly.
		('BRO', 'Broken'),
		('REP', 'In repair'),
		('RET', 'Retired (Die)'),
	)
	status = models.CharField(max_length=3, choices=STATUS)
	register_date = models.DateTimeField('date device registered', auto_now_add=True) # The register date is basically fixed. While other status could be mutable. 

	def __unicode__(self):
		return self.device_sn


class Event(models.Model):
	event_id = models.AutoField(primary_key=True)
	device = models.ForeignKey(LabDevice, on_delete=models.CASCADE)
	event = models.CharField(max_length=512) # used to store all the events expressed in JSON.

	def __unicode__(self):
		return self.event