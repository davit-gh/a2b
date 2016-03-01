# coding: utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class City(models.Model):
    name_en = models.CharField(max_length=100)
    name_hy = models.CharField(max_length=100)
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        db_table = "ab_city"
    def __unicode__(self):
            return self.name_hy


class Country(models.Model):
    name_en = models.CharField(max_length=100)
    name_hy = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        db_table = "ab_country"
    def __unicode__(self):
            return self.name_hy


class Image(models.Model):
    image = models.ImageField(upload_to="uploads/images", null=True, blank=True)
    caption = models.CharField(max_length=50, blank=True)
    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        db_table = "ab_image"
    def __unicode__(self):
            return self.image.name


class Driver(models.Model):
    mobile = models.CharField(max_length=30, blank=False)
    featured_image = models.OneToOneField(Image, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    licence_plate = models.CharField(max_length=10, default="19oo199")
    class Meta:
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"
        db_table = "ab_driver"
    def __unicode__(self):
            return self.mobile

class DriverImage(models.Model):
    driver = models.ForeignKey(Driver, related_name="imgs")
    image = models.ImageField(upload_to="uploads/images", null=True, blank=True)
    class Meta:
        verbose_name="Driver Image"
        verbose_name_plural="Driver Images"
        db_table = "ab_driverimage"

class Ride(models.Model):
    fromwhere = models.ForeignKey(City, related_name="rides_from")
    towhere = models.ForeignKey(City, related_name="rides_to")
    leavedate = models.DateField(blank=True)
    starttime = models.TimeField(blank=True)
    endtime = models.TimeField(blank=True, null=True)
    price = models.IntegerField(blank=True)
    passenger_number = models.IntegerField(blank=False, default=2)
    driver = models.ForeignKey(Driver, related_name="rides")

    class Meta:
        verbose_name = "Ride"
        verbose_name_plural = "Rides"
        db_table = "ab_ride"
    def __unicode__(self):
            return self.fromwhere

class Contactus(models.Model):
    name = models.CharField("Անուն", max_length=100, blank=False)
    email = models.EmailField("Էլ․ փոստ", blank=False)
    message = models.TextField("Նամակ", blank=False)
    message_date = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        db_table = "ab_contactus"
    def __unicode__(self):
            return self.email


class UserSearch(models.Model):
    fromwhere =  models.CharField(max_length=100, blank=False)
    towhere = models.CharField(max_length=100, blank=False)
    leavedate = models.DateField(blank=True)

    class Meta:
        verbose_name = "User Search"
        verbose_name_plural = "User Searches"
        db_table = "ab_usersearch"
    def __unicode__(self):
            return "%s - %s" % (self.fromwhere, self.towhere)


class Inboundmail(models.Model):
    html_body = models.CharField(max_length=2000)
    send_date = models.DateTimeField()
    subject = models.CharField(max_length=100)
    reply_to = models.CharField(max_length=100)
    sender = models.CharField(max_length=100)
    attachment = models.CharField(max_length=400,blank=True)

    class Meta:
        db_table = "ab_mail"
        
    def htmlify(self):
        attachment_array = self.attachment.split(',')
        return  ' '.join([format_html('<a href="{}">{}</a>', att, att.split('/')[-1]) for att in attachment_array])
    htmlify.allow_tags = True