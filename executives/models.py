from django.db import models
from authentication.models import Account

class ExecutiveProfile(models.Model):
    executive = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    document_url = models.CharField(max_length=100, null=True, blank=True)