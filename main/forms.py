from main.models import City, Ride
from django.forms import ModelForm, Textarea
from django import forms
from django.utils.translation import ugettext as _
from functools import partial
DateInput = partial(forms.DateInput, )

# Form Fields
from django.utils import timezone
from datetimewidget.widgets import DateTimeWidget
from datetimewidget.widgets import DateWidget
import datetime
import pdb

class RidesearchForm(ModelForm):

        
	fromwhere   = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name="name_hy", widget=forms.Select(attrs={"onChange":'sourcefilter(this)'}))
	towhere 	= forms.ModelChoiceField(queryset=City.objects.all(), to_field_name="name_hy", widget=forms.Select(attrs={"onChange":'destfilter(this)'}))
	class Meta:
 		model = Ride
		fields = ['fromwhere', 'towhere', 'leavedate']

		widgets = {
            		'leavedate': DateTimeWidget(attrs={'id':"id_source"}, options={'startDate':'+1d'}),
       	}

	def clean_start_date(self):
		leave_datetime = self.cleaned_data["leavedate"]
		leave_date = leave_datetime.date()
		curr_date = datetime.datetime.now().date()
		if leave_date < curr_date + datetime.timedelta(days=1):
		    raise forms.ValidationError(_("Please enter future date."), code='invalid')
		return leave_datetime

		
class RideAdminForm(ModelForm):

        
	fromwhere   = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name="name_hy")
	towhere 	= forms.ModelChoiceField(queryset=City.objects.all(), to_field_name="name_hy")
	class Meta:
 		model = Ride
		fields = ['fromwhere', 'towhere', 'leavedate', 'endtime', 'howmuch', 'driver']
		

