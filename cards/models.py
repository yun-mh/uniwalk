from django.db import models


class Card(models.Model):
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    card_id = models.CharField(max_length=50, blank=True, null=True)
    fingerprint = models.CharField(max_length=50, blank=True, null=True)
    exp_month = models.CharField(max_length=50, blank=True, null=True)
    exp_year = models.CharField(max_length=50, blank=True, null=True)
