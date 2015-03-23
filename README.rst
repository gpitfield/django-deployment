=====
Django Deployments
=====

Django Deployments provides a simple model to keep track of mobile or
web product releases, and a set of management commands to streamline
code deployment to AWS servers.

Quick start
-----------

1. Add "deployments" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'deployments',
    )
	
2. Run `python manage.py migrate` to create the diagnostics models.

4. Configure settings::

    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    SERVER_KEYPATH = '/local/path/to/ssh/key'
    UPDATE_SCRIPT = '/server/path/to/update/script'