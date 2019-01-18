from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class UnifiUser(models.Model):
    """Base module registered unifi user."""

    user = models.ForeignKey(User)
    guest_mac = models.CharField(max_length=255, null=True)
    last_backend_login = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        return self.user.email

    def __str__(self):
        return self.user.email
