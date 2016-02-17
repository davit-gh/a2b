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

    def __unicode__(self):
            return self.name_hy


class Driver(models.Model):
    mobile = models.CharField(max_length=30, blank=False)
    featured_image = models.ImageField(upload_to="uploads", null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"
    
    def __unicode__(self):
            return self.mobile

class DriverCarImage(models.Model):
    driver = models.ForeignKey(Driver, related_name="images")
    image = models.ImageField(upload_to="uploads/cars", null=True, blank=True)
    class Meta:
        verbose_name="Driver Car Image"
        verbose_name_plural="Driver Car Images"

class Ride(models.Model):
    fromwhere = models.CharField("From", max_length=100, blank=False)
    towhere = models.CharField("To", max_length=100, blank=False)
    leavedate = models.DateTimeField(blank=True)
    endtime = models.TimeField(blank=True)
    howmuch = models.IntegerField(blank=True)
    driver = models.ForeignKey(Driver, related_name="rides")

    class Meta:
        verbose_name = "Ride"
        verbose_name_plural = "Rides"
    
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
    
    def __unicode__(self):
            return self.email


class UserSearch(models.Model):
    fromwhere = models.CharField(max_length=100, blank=False)
    towhere = models.CharField(max_length=100, blank=False)
    leavedate = models.DateField(blank=True)

    class Meta:
        verbose_name = "User Search"
        verbose_name_plural = "User Searches"
    
    def __unicode__(self):
            return self.email