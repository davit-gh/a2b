# coding: utf-8
import django_tables2 as tables
from main.models import Ride
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

class DriverColumn(tables.Column):
    def render(self, record):
        return mark_safe('<img id="driver-img" width="150px" data-id=' + str(
            record.driver.id) + ' data-toggle="modal" data-target="#myModal" src="%s" />' % escape(
            record.driver.featured_image.image.url))


class RideTable(tables.Table):
    leavedate = tables.Column(verbose_name="Ամսաթիվ")
    starttime = tables.Column(verbose_name="Ժամ")
    price = tables.Column(verbose_name="Արժեքը")
    fromwhere = tables.Column(verbose_name="Որտեղից")
    towhere = tables.Column(verbose_name="Ուր")



    def render_leavedate(self, value, record):
        return record.leavedate.strftime('%d - %m - %Y')

    class Meta:
        model = Ride
        attrs = {"class": "table table-hover"}
        exclude = ("id", "endtime", "driver", "passenger_number")
        empty_text = "Ներկայումս մենք չունենք Ձեր ուղղությամբ երթուղիներ, այցելեք մեզ ավելի ուշ։"



class DriverRideTable(tables.Table):
    leavedate = tables.Column(verbose_name="Ամսաթիվ")
    starttime = tables.Column(verbose_name="Ժամ")
    price = tables.Column(verbose_name="Արժեքը")
    fromwhere = tables.Column(verbose_name="Որտեղից")
    towhere = tables.Column(verbose_name="Ուր")
    passenger_number = tables.Column("Ազատ տեղեր")
    delete = tables.Column(verbose_name="Ջնջե՞լ", orderable=False, empty_values=())



    def render_leavedate(self, value, record):
        return record.leavedate.strftime('%d - %m - %Y')

    def render_delete(self, value, record):
        return mark_safe('<i id=' + str(record.id) + ' data-toggle="modal" data-target="#confirm" class="fa fa-times fa-2x"></i>')

    class Meta:
        model = Ride
        attrs = {"class": "table table-hover"}
        exclude = ("id", "endtime", "driver")
        empty_text = "Ներկայումս մենք չունենք Ձեր ուղղությամբ երթուղիներ, այցելեք մեզ ավելի ուշ։"
