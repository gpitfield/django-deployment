import os, sys
import urllib
from boto.ec2.connection import EC2Connection
from django.conf import settings

def environment():
	ENVIRONMENT = os.environ.get('ENVIRONMENT')
	IS_TEST = any([el in sys.argv for el in ('test', 'deploy')])
	IS_DEVELOPMENT = ENVIRONMENT == 'dev' and not IS_TEST
	if IS_DEVELOPMENT:
		return 'development'
	elif IS_TEST:
		return 'testing'
	try:
		this_instance_id = urllib.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read()
	except IOError:
		return None
	ec2_conn = EC2Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
	this_instance = ec2_conn.get_all_instances(this_instance_id)[0].instances[0]
	return this_instance.tags.get('environment', None)