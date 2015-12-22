from django.shortcuts import render
from main.models import Driver
from main.forms import RidesearchForm, ContactusForm
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json, pdb
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
	drivers = Driver.objects.all()
		
	return render(request,'main/pages/index.html',{'form':form, 'drivers': drivers})
	
def ridesearch(request):
	if request.method == 'POST':
		items = PortfolioItem.objects.filter(categories__slug=request.POST['towhere'])
		form = RidesearchForm(request.POST)
		if form.is_valid():
			form.save()
	else:
		form = RidesearchForm()
		items = PortfolioItem.objects.all()
	#pdb.set_trace()
	return render(request, 'main/pages/index.html', {'items': items})

def get_car_images(request):
	if request.method == 'POST' and request.is_ajax():
		id = request.POST.get('id','')
		driver = get_object_or_404(Driver, id = id)
		images = map(lambda x: x.image.url, driver.images.all())
		#pdb.set_trace()
		return JsonResponse({'images': images, 'name': driver.name, 'mobile': driver.mobile })
