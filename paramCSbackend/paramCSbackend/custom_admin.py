from django.contrib.admin.models import LogEntry

class CustomLogEntry(LogEntry):
    class Meta(LogEntry.Meta):
        managed = False
        db_table = 'django_admin_log'
