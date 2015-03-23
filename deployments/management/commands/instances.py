#!/usr/bin/pythonv

import subprocess
import sys, os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from boto.ec2.connection import EC2Connection

AWS_ACCESS_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
SERVER_KEYPATH = getattr(settings, 'SERVER_KEYPATH', None)
UPDATE_SCRIPT = getattr(settings, 'UPDATE_SCRIPT', None)

def enumerate_instances(update=False, monitor=False):
	project_name = os.path.split(settings.BASE_DIR)[1]
	ec2_conn = EC2Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
	reservations = ec2_conn.get_all_instances()
	print 'Please enter the number of the instance to connect to:'
	i = 1
	instances = []
	for reservation in reservations:
		for instance in reservation.instances:
			if instance.state == 'running':
				if instance.tags.get('project', None) in [project_name, None]:
					instances.append(instance.dns_name)
					instance_name = ' - %s'%instance.tags['Name'] if 'Name' in instance.tags else ''
					print '[%d] %s (%s)%s'%(i, str(instance.dns_name), str(instance.instance_type), instance_name)
					i = i + 1
	selection = raw_input()
	if selection:
		selection = selection.split(',')
		selection = [int(sel) for sel in selection]
	else:
		selection = None
	if update:
		for instance in instances:
			update = False if (selection and not (instances.index(instance)+1) in selection) else True
			if not UPDATE_SCRIPT:
				print 'Please supply the location of the UPDATE_SCRIPT in your settings.'
			elif update:
				connect = ['ssh', '-i', SERVER_KEYPATH, '-t', 'ec2-user@' + instance]
				script = connect + ['sudo ', UPDATE_SCRIPT, 'canary']
				subprocess.call(script)
	elif monitor:
		selection = selection[0]
		connect = ['ssh', '-i', SERVER_KEYPATH, '-t', 'ec2-user@' + instances[selection-1]]
		script = connect + ['sudo tail -f /var/log/httpd/access_log']
		subprocess.call(script)
	else:
		selection = selection[0]
		print 'Connecting to ' + instances[selection - 1] + '...'
		connect = ['ssh', '-i', SERVER_KEYPATH, 'ec2-user@' + instances[selection-1]]
		subprocess.call(connect)

class Command(BaseCommand):
	args = '<update>'
	help = 'Deploy code base to production environment.'

	def handle(self, *args, **options):
		update = len(args) > 0
		return enumerate_instances(update)
