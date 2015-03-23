from django.db import models
from django.contrib.auth.models import User

class ReleaseChecklist(models.Model):
	version_number = models.CharField(max_length=12)
	build_number = models.CharField(max_length=8, null=True, blank=True)
	platform = models.CharField(max_length=20, choices=(('Android', 'Android'), ('iOS', 'iOS')))
	release_date = models.DateField(null=True, blank=True)
	released_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	commit_sha = models.CharField(max_length=256, null=True, blank=True)
	# checks
	uses_prod = models.BooleanField('Uses production settings', default=False)
	secure_http = models.BooleanField('Verify https and MITM security', default=False)
	push_notify = models.BooleanField('Verify push notifications, including aps-environment value', default=False)
	ssl_cert_valid = models.BooleanField('Verify SSL validity', default=False)
	bad_email_check = models.BooleanField('Handles bad email error', default=False)
	bad_domain_check = models.BooleanField('Handles bad domain error', default=False)	
	bad_auth_check = models.BooleanField('Handles permission denied error', default=False)