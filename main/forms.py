#!/usr/bin/env python
# -*- coding: utf-8 -*-

from main.models import City, Ride, Contactus, UserSearch
from django.forms import ModelForm, Textarea
from django import forms
from django.utils.translation import ugettext as _
from functools import partial
DateInput = partial(forms.DateInput, )

# Form Fields
from django.utils import timezone
from datetimewidget.widgets import DateTimeWidget
from datetimewidget.widgets import DateWidget
from datetime import datetime
import pdb



class UserSearchForm(ModelForm):
	
     
	fromwhere   = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Բոլորը", to_field_name="name_hy", widget=forms.Select(attrs={"onChange":'sourcefilter(this)'}))
	towhere 	= forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Բոլորը", to_field_name="name_hy", widget=forms.Select(attrs={"onChange":'destfilter(this)'}))
	leavedate   = forms.CharField(widget=DateWidget(attrs={'id':"id_source"}, options={'startDate':'+1d'}))
	class Meta:
 		model = UserSearch
		fields = ['fromwhere', 'towhere', 'leavedate']

	def clean_leavedate(self):
		#pdb.set_trace()
		leave_datetime = self.cleaned_data["leavedate"]
		leave_date = datetime.strptime(leave_datetime,'%d/%m/%Y')
	
		return leave_date.strftime('%Y-%m-%d')
		
class RideAdminForm(ModelForm):

        
	fromwhere   = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name="name_hy")
	towhere 	= forms.ModelChoiceField(queryset=City.objects.all(), to_field_name="name_hy")
	class Meta:
 		model = Ride
		fields = ['fromwhere', 'towhere', 'leavedate', 'endtime', 'howmuch', 'driver']
		

class ContactusForm(ModelForm):
	class Meta:
		model = Contactus
		fields = ['name', 'email', 'message']
