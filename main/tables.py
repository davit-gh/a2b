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
    leavedate = tables.Column(verbose_name=_("Date"))
    starttime = tables.Column(verbose_name=_("Time"))
    price = tables.Column(verbose_name=_("Price"))
    fromwhere = tables.Column(verbose_name=_("From where"))
    towhere = tables.Column(verbose_name=_("To where"))
    details = tables.Column(verbose_name=_("Details"), orderable=False, empty_values=())


    def render_leavedate(self, value, record):
        return record.leavedate.strftime('%d - %m - %Y')

    def render_details(self, value, record):
        return mark_safe('<a class="" href="%s">%s</a>' % ("/ride/"+record.uuid, _("Details")))

    class Meta:
        model = Ride
        attrs = {"class": "table table-bordered"}
        exclude = ("id", "endtime", "driver", "passenger_number", "uuid")
        empty_text = _("Currently there are no rides matching your search, check back later, please.")#



class DriverRideTable(tables.Table):
    leavedate = tables.Column(verbose_name=_("Date"))
    starttime = tables.Column(verbose_name=_("Time"))
    price = tables.Column(verbose_name=_("Price"))
    fromwhere = tables.Column(verbose_name=_("From where"))
    towhere = tables.Column(verbose_name=_("To where"))
    passenger_number = tables.Column(verbose_name=_("Free seats"))
    delete = tables.Column(verbose_name=_("Delete"), orderable=False, empty_values=())



    def render_leavedate(self, value, record):
        return record.leavedate.strftime('%d - %m - %Y')

    def render_delete(self, value, record):
        return mark_safe('<i id=' + str(record.id) + ' data-toggle="modal" data-target="#confirm" class="fa fa-times fa-2x"></i>'
                        '<i id=' + record.uuid + ' data-toggle="modal" data-target="#quickview" class="fa fa-eye fa-2x"></i>')

    class Meta:
        model = Ride
        attrs = {"class": "table table-bordered", "id": "ride_table"}
        exclude = ("id", "endtime", "driver", "uuid")
        empty_text = _("You haven't added any routes yet, go ahead and add the first one!")
