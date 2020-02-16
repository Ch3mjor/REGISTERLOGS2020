from django.contrib.postgres.fields import JSONField
from django.db import models


class RequestLog(models.Model):
    ip_addr = models.GenericIPAddressField(null=True, blank=False)
    browser = models.CharField(max_length=50, blank=False, null=False)
    ctype = models.CharField(max_length=30, blank=False, null=False)
    query = JSONField(default=dict, null=False)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f'{self.ip_addr}-{self.browser}'
