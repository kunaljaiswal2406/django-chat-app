#!/usr/bin/env python
"""Models for the test_challenge app."""


from django.db import models

from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, db_index=True, on_delete=models.CASCADE, related_name="receiver"
    )
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now=True)
    read_at = models.DateTimeField(null=True)
    is_read = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_message_as_read(self):
        self.is_read = True
        self.save()
