#!/usr/bin/pythonv

import sys,os
import datetime, time, subprocess
import git
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from instances import enumerate_instances

TEST_APPS = ['feed', 'profiles', 'companies', 'api',]


class Command(BaseCommand):
	args = ''
	help = 'Monitor apache logs on an instance.'


	def handle(self, *args, **options):
		enumerate_instances(monitor=True)