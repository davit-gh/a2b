from django.shortcuts import render
from main.models import Driver, HowItWorks, Ride
from main.tables import RideTable
from main.forms import UserSearchForm, ContactusForm
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_tables2   import RequestConfig
import json, pdb, datetime
# Create your views here.
def contactus(request):
	if request.method == 'POST':
        	form = ContactusForm(request.POST)
        # check whether it's valid:
        	if form.is_valid():
            	# process the data in form.cleaned_data as required
            		form.save()
            		form = ContactusForm()
            	# redirect to a new URL:
			messages.info(request, _("We received your message, we will respond shortly. Thank you!"))
		else:
			messages.error(request, _("Your message has not been sent. Please fill in all the fields."))
    	# if a GET (or any other method) we'll create a blank form
    	else:
        	form = ContactusForm()
	rides = Ride.objects.all()
	howitworks = get_object_or_404(HowItWorks, pk=1)
	table = RideTable(rides)
	RequestConfig(request, paginate={"per_page": 3}).configure(table)
	return render(request,'main/pages/index.html',{'form':form, 'table': table, 'howitworks': howitworks.desc })
	
def ridesearch(request):
	if request.method == 'POST':
		form = UserSearchForm(request.POST)
		if form.is_valid():
			post_dict = request.POST
			d = datetime.datetime.strptime(post_dict['leavedate'], '%d/%m/%Y')
			rides = Ride.objects.filter(fromwhere=post_dict['fromwhere'], towhere=post_dict['towhere'], leavedate__year=d.year, leavedate__month=d.month, leavedate__day=d.day)
			form.save()
	else:
		form = UserSearchForm()
		rides = Ride.objects.all()
		#items = PortfolioItem.objects.all()
	#pdb.set_trace()
	table = RideTable(rides)
	RequestConfig(request).configure(table)
	form = ContactusForm()
	howitworks = get_object_or_404(HowItWorks, pk=1)
	return render(request, 'main/pages/index.html', {'table': table, 'form':form, 'howitworks': howitworks.desc })

def get_car_images(request):
	if request.method == 'POST' and request.is_ajax():
		id = request.POST.get('id','')
		driver = get_object_or_404(Driver, id = id)
		images = map(lambda x: x.image.url, driver.images.all())
		#pdb.set_trace()
		return JsonResponse({'images': images, 'name': driver.name, 'mobile': driver.mobile })
