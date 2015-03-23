#!/usr/bin/pythonv

import sys,os
import datetime, time, subprocess
import git
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from instances import enumerate_instances
from django.apps import apps

TEST_APPS = [app for app in settings.INSTALLED_APPS if not app.startswith('django')]

class Command(BaseCommand):
	args = ''
	help = 'Deploy code base to production environment.'

	def run_tests(self, apps):
		if apps:
			self.stdout.write('testing %s'%', '.join(apps))
			call_command('test', *apps)

	def do_test(self):
		self.stdout.write('Which modules do you want to test?')
		self.stdout.write('Press [enter] to test all, 0 for none, * to test only (no repo push)')
		i = 1
		deploy = True
		for app in TEST_APPS:
			self.stdout.write('[' + str(i) + '] ' + app)
			i = i + 1
		selection = raw_input()
		if selection:
			selection = selection.split(',')
			if '*' in selection:
				deploy = False
				selection.remove('*')
		if selection:
			selection = [TEST_APPS[int(sel)-1] for sel in selection if int(sel)>0]
		else:
			selection = TEST_APPS
		self.run_tests(selection)
		return deploy


	def handle(self, *args, **options):
		deploy = self.do_test()
		if deploy:
			repo = git.Repo(settings.BASE_DIR)
			if repo.head.reference in [repo.heads.master]:#, repo.heads.production]: # we only push production branches
				if not repo.is_dirty():
					self.stdout.write('Pushing repo to origin.')
					origin = repo.remotes.origin  # get default remote by name
					origin.push()
					self.stdout.write('Deploy to servers')
					enumerate_instances(True)
					self.stdout.write('Deployment complete.')
				else:
					self.stdout.write('Abandoning deployment - please commit your changes prior to deployment.')
			else:
				self.stdout.write('Please switch to branch production')