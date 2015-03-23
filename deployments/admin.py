from django.contrib import admin
from models import ReleaseChecklist

class ReleaseChecklistAdmin(admin.ModelAdmin):
    list_display = ['version_number', 'platform', 'release_date', 'commit_sha']
    fieldsets = (
        (None, {
            'fields': ('version_number', 'build_number', 'platform',
                'release_date', 'commit_sha', 'released_by'
            )
        }),
        ('Checklist', {
            # 'classes': ('collapse',),
            'fields': ('uses_prod', 'push_notify', 'secure_http', 'ssl_cert_valid',
                'bad_email_check', 
                'bad_domain_check', 'bad_auth_check'
            )
        }),
    )

        
admin.site.register(ReleaseChecklist, ReleaseChecklistAdmin)
