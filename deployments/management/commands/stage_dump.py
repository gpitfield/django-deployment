#!/usr/bin/pythonv

import sys
import subprocess
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_app, get_models

class Command(BaseCommand):
	args = "<restore_db>"
	help = 'Dump data to staging database. restore_db should be either "staging" or "development". Always copies from database "production".'


	def handle(self, *args, **options):
		prod = settings.DATABASES['production']
		restore = settings.DATABASES[args[0]]
		dump_script = 'pg_dump -h %s -p %s -U %s -W -Fc -f stage_dump.sql %s'
		dump_script = dump_script%(prod['HOST'], prod['PORT'], prod['USER'], prod['NAME'])
		sys.stdout.write('Prod PW: %s\n'%prod['PASSWORD'])
		subprocess.call(dump_script.split())

		if args[0] == 'staging':
			restore_script = 'pg_restore -d %s -h %s -p %s -U %s -W -Fc -c stage_dump.sql'
			restore_script = restore_script%(restore['NAME'], restore['HOST'], restore['PORT'], restore['USER'])
		elif args[0] == 'development':
			restore_script = 'pg_restore -d %s -U %s -W -Fc -c stage_dump.sql'
			restore_script = restore_script%(restore['NAME'], restore['USER'])
		sys.stdout.write('%s DB PW: %s\n'%(args[0], restore['PASSWORD']))
		subprocess.call(restore_script.split())

