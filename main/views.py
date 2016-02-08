# coding: utf-8
from django.shortcuts import render, redirect
from main.models import Driver, Ride
from main.tables import RideTable
from main.forms import UserSearchForm, ContactusForm, LoginForm, ProfileForm
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_tables2   import RequestConfig
import json, pdb, datetime
from django.contrib import messages
from django.contrib.auth import (authenticate, login as auth_login,
                                               logout as auth_logout)

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
			messages.info(request, "Մենք ստացանք Ձեր նամակը և շուտով կպատասխանենք։ Շնորհակալություն։")
		else:
			messages.error(request, _("Your message has not been sent. Please fill in all the fields."))
    	# if a GET (or any other method) we'll create a blank form
    	else:
        	form = ContactusForm()
	rides = Ride.objects.all()
	loginform = LoginForm(prefix="login")
	table = RideTable(rides)
	RequestConfig(request, paginate={"per_page": 3}).configure(table)
	return render(request,'main/pages/index.html',{'form':form, 'table': table, 'loginform': loginform})
	
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
	return render(request, 'main/pages/index.html', {'table': table, 'form':form})

def get_car_images(request):
	if request.method == 'POST' and request.is_ajax():
		id = request.POST.get('id','')
		driver = get_object_or_404(Driver, id = id)
		images = map(lambda x: x.image.url, driver.images.all())
		#pdb.set_trace()
		return JsonResponse({'images': images, 'name': driver.name, 'mobile': driver.mobile })


def logout(request):
    """
    Log the user out.
    """
    auth_logout(request)
    messages.info(request, "Successfully logged out")
    return redirect('/')

def signup(request, template="main/register.html"):
    """
    Signup form.
    """
    """
    Login form.
    """
    login_form = LoginForm(prefix="login")
    signup_form = ProfileForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST, prefix="login")
        signup_form = ProfileForm(request.POST)
        if not login_form.has_changed() and not request.POST.get("from_popup",False): login_form = LoginForm(prefix="login")
        if not signup_form.has_changed(): signup_form = ProfileForm()
        
        if login_form.is_valid():
            authenticated_user = login_form.save()
            messages.info(request, "Successfully logged in")
            auth_login(request, authenticated_user)
            
            return redirect('/')

        if signup_form.has_changed() and signup_form.is_valid():
            #import pdb;pdb.set_trace()
            new_user = signup_form.save()
            messages.info(request, "Successfully signed up")
            auth_login(request, new_user)
            return redirect("/")
    #import pdb;pdb.set_trace()
    context = {"login_form": login_form, "signup_form": signup_form}
    return render(request, template, context)