# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Building(models.Model):
    b_name = models.CharField(max_length=50, null=False)
    b_addr = models.CharField(max_length=100, null=False)
    b_postcode = models.IntegerField(null=True)
    b_type = models.CharField(max_length=20, null=True)
    b_grosssize = models.IntegerField(null=True)
    b_airconsize = models.IntegerField(null=True)

    def __unicode__(self):
        return self.b_name

    class Meta:
        abstract = False
        verbose_name = "Building Information"


class BaseLogging(models.Model):
    time_stamp = models.DateTimeField(null=False)
    chwshdr = models.FloatField(default=0.0, null=True)
    chwrhdr = models.FloatField(default=0.0, null=True)
    chwfhdr = models.FloatField(default=0.0, null=True)
    cwshdr = models.FloatField(default=0.0, null=True)
    cwrhdr = models.FloatField(default=0.0, null=True)
    cwfhdr = models.FloatField(default=0.0, null=True)
    ch1kw = models.FloatField(default=0.0, null=True)
    chwp1kw = models.FloatField(default=0.0, null=True)
    cwp1kw = models.FloatField(default=0.0, null=True)
    ct1kw = models.FloatField(default=0.0, null=True)

    class Meta:
        abstract = True
        verbose_name = "Base Logging Metrics"


class JPLogging(BaseLogging):
    # Add new logging metrics at Jurong Point site
    ch2kw = models.FloatField(default=0.0, null=True)
    ch3kw = models.FloatField(default=0.0, null=True)
    ch4kw = models.FloatField(default=0.0, null=True)
    ch5kw = models.FloatField(default=0.0, null=True)
    ch6kw = models.FloatField(default=0.0, null=True)

    chwp2kw = models.FloatField(default=0.0, null=True)
    chwp3kw = models.FloatField(default=0.0, null=True)
    chwp4kw = models.FloatField(default=0.0, null=True)
    chwp5kw = models.FloatField(default=0.0, null=True)
    chwp6kw = models.FloatField(default=0.0, null=True)

    cwp2kw = models.FloatField(default=0.0, null=True)
    cwp3kw = models.FloatField(default=0.0, null=True)
    cwp4kw = models.FloatField(default=0.0, null=True)
    cwp5kw = models.FloatField(default=0.0, null=True)
    cwp6kw = models.FloatField(default=0.0, null=True)

    ct2kw = models.FloatField(default=0.0, null=True)
    ct3kw = models.FloatField(default=0.0, null=True)
    ct4kw = models.FloatField(default=0.0, null=True)
    ct5kw = models.FloatField(default=0.0, null=True)
    ct6kw = models.FloatField(default=0.0, null=True)

    def __unicode__(self):
        return self.time_stamp

    class Meta:
        abstract = False
        verbose_name = "Jurong Point Logging Table"


class SAALogging(BaseLogging):
    # Add new logging metrics at SSA site
    ch2kw = models.FloatField(default=0.0, null=True)
    chwp2kw = models.FloatField(default=0.0, null=True)
    cwp2kw = models.FloatField(default=0.0, null=True)
    ct2kw = models.FloatField(default=0.0, null=True)

    def __unicode__(self):
        return self.time_stamp

    class Meta:
        abstract = False
        verbose_name = "SSA Logging Table"


BUILDING_LIST = (
    ('jurongpoint', 'Jurong Point'),
    ('saa', 'SAA Campus'),
    ('bedokpoint', 'Bedok Point'),
    ('insead', 'Insead Campus'),
    ('kingshotel', 'King\'s Hotel'),
)

OPTION_LIST = (
    ('kaer', 'KAER-Header'),
    ('sys', 'KAER-SYS'),
    ('check', 'KAER_Check'),
)


class PageToRender(models.Model):
    page_name = models.CharField(default="pagetorender", max_length=50)
    building_choice = models.CharField(max_length=50, choices=BUILDING_LIST)
    options = models.CharField(max_length=50, choices=OPTION_LIST)
    from_date = models.DateField(null=True)
    from_time = models.TimeField(null=True)
    to_date = models.DateField(null=True)
    to_time = models.TimeField(null=True)

    def __unicode__(self):
        return self.page_name

    class Meta:
        abstract = False
        verbose_name = "Items Shown on Enquiry Page"