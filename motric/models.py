from __future__ import unicode_literals

from django.db import models

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
	device_label = models.CharField(max_length=30)

	def __unicode__(self):
		return self.ldap

class RequestedDevice(DeviceStatus):
	model_type = models.CharField(max_length=30)
	quantity = models.IntegerField(default=1)
	os_version = models.CharField(max_length=50)
	requester = models.ForeignKey(Requester, on_delete=models.CASCADE)
	request_date = models.DateTimeField(auto_now_add=True) 
	approve_date = models.DateTimeField(blank=True, null=True, editable=False)
	lab_location = models.CharField(max_length=3, blank=True, null=True)
	po_number = models.CharField(max_length=50, blank=True)
	po_date = models.DateTimeField(blank=True, null=True)
	price_usd = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
	price_cny = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
	ex_rate = models.FloatField(blank=True, null=True)
	resolved = models.BooleanField(default=False)

	def __unicode__(self):
		return u'%s, with os %s, requested by %s, for %s project' % (self.model_type, self.os_version, self.requester.ldap, self.requester.project)
		# return self.model_type

class LabDevice(DeviceStatus):
	# model = models.OneToOneField(RequestedDevice)
	model = models.ForeignKey(RequestedDevice)
	device_sn = models.CharField(max_length=100)
	register_date = models.DateTimeField('date device_sn recorded', auto_now_add=True) # The register date is basically fixed. While other status could be mutable. 

	def __unicode__(self):
		return self.device_sn


class Event(models.Model):
	event_id = models.AutoField(primary_key=True)
	device = models.ForeignKey(LabDevice, on_delete=models.CASCADE)
	event = models.CharField(max_length=512) # used to store all the events expressed in JSON.

	def __unicode__(self):
		return self.event