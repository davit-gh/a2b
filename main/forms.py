#from ajax_select import make_ajax_field
#from ajax_select import make_ajax_form
#from main.models import SourceDest
from main.models import City
from django.forms import ModelForm, Textarea
from ajax_select.fields import AutoCompleteField
from ajax_select.fields import AutoCompleteWidget
from django import forms
from functools import partial
from django.utils.translation import ugettext as _

DateInput = partial(forms.DateInput, )

# Form Fields
from django.utils import timezone
from datetimewidget.widgets import DateTimeWidget
from datetimewidget.widgets import DateWidget
from main.models import Ridesearch
import datetime
import pdb

class RidesearchForm(ModelForm):


	PASSANGER_NUMBER_CHOICES = (
            (1, '1 passanger'),
            (2, '2 passanger'),
            (3, '3 passanger'),
        )
        
	fromwhere   = AutoCompleteField('city', label=_('Source'), required=True, help_text=None)
	towhere 	= forms.ModelChoiceField(queryset=City.objects.all(), to_field_name="name_en")
	passanger_number = forms.ChoiceField(label=_("How many?"), widget=forms.Select(attrs={'id': "id_passanger_number", 'class': 'passnumClass'}), choices=PASSANGER_NUMBER_CHOICES)
#	payment_method = forms.ChoiceField(label=_("Payment Method"), choices=PAYMENT_CHOICES, widget=forms.RadioSelect(), initial='1')
	class Meta:
 		model = Ridesearch
		fields = ['fromwhere', 'towhere', 'leavedate', 'passanger_number']

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

		
