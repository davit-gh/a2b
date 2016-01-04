# coding: utf-8
import django_tables2 as tables
from main.models import Ride
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
import pdb
class DriverColumn(tables.Column):
	def render(self, record):
		return mark_safe('<img id="driver-img" data-id='+str(record.driver.id) +' data-toggle="modal" data-target="#myModal" src="%s" />' % escape(record.driver.featured_image.url))

class RideTable(tables.Table):
	leavedate = tables.Column(verbose_name="Ամսաթիվ")
	driver 	  = DriverColumn(verbose_name="Վարորդ")
	howmuch   = tables.Column(verbose_name="Արժեքը")
	fromwhere = tables.Column(verbose_name="Որտեղից")
	towhere   = tables.Column(verbose_name="Ուր")
	def render_leavedate(self, value, record):
		#pdb.set_trace()
		return "%s - %s" % (value.strftime('%d/%m/%Y %H:%M'), record.endtime.strftime("%H:%M"))

	class Meta:
		model = Ride
		attrs = {"class": "table table-hover"}
		exclude = ("id","endtime",)
