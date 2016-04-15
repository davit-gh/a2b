# coding: utf-8
from django.shortcuts import render, redirect
from main.models import Ride, Driver, CarImage, City, Car
from main.tables import RideTable, DriverRideTable
from main.forms import UserSearchForm, ContactusForm, LoginForm, ProfileForm, RideAdminForm, CarForm, DriverForm, BaseCarimageFormset, UserForm
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_tables2   import RequestConfig
import json, pdb, datetime, uuid
from django.contrib import messages
from django.contrib.auth import (authenticate, login as auth_login,
                                               logout as auth_logout)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import formset_factory, inlineformset_factory
from django import forms
from main.models import Inboundmail
from postmark_inbound import PostmarkInbound
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseBadRequest

# Create your views here.
def contactus(request, template='main/pages/base.html'):
    
    form = UserSearchForm()
    
    return render(request, template, {'form': form})
		
	
def index(request):
    
    
    #table = RideTable(rides)
    #RequestConfig(request, paginate={"per_page": 3}).configure(table)

    if request.method == "POST":
        form = UserSearchForm(request.POST)
        
        if form.is_valid():
            kwargs = {}
            data = form.cleaned_data
            if not form.has_changed():
                rides = Ride.objects.all()
                
            else:
                
                for k,v in data.items():
                    if v:
                        kwargs[k] = v
                rides = Ride.objects.filter(**kwargs)
            form.save()
            table = RideTable(rides)
            RequestConfig(request, paginate={"per_page": 3}).configure(table)
            return render(request, 'main/pages/index.html', {'form': form, 'table': table})
    else:
        form = UserSearchForm()
    rides = Ride.objects.all()
    table = RideTable(rides)
    RequestConfig(request, paginate={"per_page": 3}).configure(table)
    return render(request, 'main/pages/index.html', {'table': table, 'form':form})

def get_car_images(request):
	if request.method == 'POST' and request.is_ajax():
		id = request.POST.get('id','')
		driver = get_object_or_404(Driver, id = id)
		images = map(lambda x: x.image.url, driver.images.all())
		#pdb.set_trace()
		return JsonResponse({'images': images, 'name': driver.user.username, 'mobile': driver.mobile })


def logout(request):
    """
    Log the user out.
    """
    auth_logout(request)
    messages.info(request, _("Successfully logged out."))
    return redirect('/')

def signup(request, template="main/register.html"):
    """
    Signup form.
    """
    loginform = LoginForm(prefix="login")
    signup_form = ProfileForm(prefix="signup")
    #import pdb; pdb.set_trace()
    if request.method == "POST":
        signup_form = ProfileForm(request.POST, prefix="signup")
        #
        if signup_form.is_valid():
            new_user = signup_form.save()
            d = Driver(user=new_user)
            d.save()
            
            messages.info(request, _("Successfully signed up!"))
            auth_login(request, new_user)
            return redirect("home")

    context = {"loginform": loginform, "signup_form": signup_form}
    return render(request, template, context)

def login(request, template="main/register.html"):
    """
    Login form.
    """
    loginform = LoginForm(prefix="login")
    signup_form = ProfileForm(prefix="signup")
    if request.method == "POST":
        #import pdb;pdb.set_trace()

        loginform = LoginForm(request.POST, prefix="login")
        if loginform.is_valid():
            authenticated_user = loginform.save()
            messages.info(request, _("Successfully logged in"))
            auth_login(request, authenticated_user)            
            return redirect('home')
    context = {"loginform": loginform, "signup_form": signup_form}
    return render(request, template, context)

@login_required
def profile_update(request, template="main/pages/account_profile_update.html"):
    """
    Profile update form.
    """
    
    profile_form = ProfileForm
    #DriverImageFormSet = inlineformset_factory(Driver, DriverImage, fields=('image',), max_num=6, extra=0,
    #                        widgets={'image': forms.FileInput()})
    
    #driver = Driver.objects.get(user=request.user)
   
    if request.method == "POST":
        form = profile_form(request.POST,
                            instance=request.user)
        #formset = DriverImageFormSet(request.POST, request.FILES, instance=driver)
        
        #import pdb;pdb.set_trace()
        #featured = request.FILES.get('featured_image', None)
        if form.is_valid() and formset.is_valid():
            #import pdb;pdb.set_trace()
            #driver.mobile = request.POST.get('mobile', None)
            #if featured:
            #    img = Image.objects.get(id=driver.featured_image.id)
            #    img.image = featured
            #    img.save()
            #driver.images = 
            #driver.save()
            form.save()
            #if formset.has_changed(): 
            #    formset.save()
            messages.info(request, _("Profile updated"))
            return redirect("/")
    else:
        form = profile_form(instance=request.user)#;
        #formset = DriverImageFormSet(instance=driver)
    context = {"form": form}
    return render(request, template, context)


@login_required
def rides(request, template="main/account/rides.html"):
    # if this is a POST request we need to process the form data
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        rideform = RideAdminForm(request.POST, user=request.user)
        #import pdb;pdb.set_trace()
        # check whether it's valid:
        if rideform.is_valid():
            # process the data in form.cleaned_data as required
            ride = rideform.save(commit=False)
            ride.driver = request.user.driver
            ride.starttime = datetime.datetime.now()
            ride.uuid = uuid.uuid4().hex
            ride.save()
            messages.info(request, _("The route is added"))
            return redirect('rides')
        
    # if a GET (or any other method) we'll create a blank form
    else:
        rideform = RideAdminForm(user=request.user)
    rides = request.user.driver.rides.all() if hasattr(request.user, 'driver') else []
        #items = PortfolioItem.objects.all()
    table = DriverRideTable(rides)
    RequestConfig(request, paginate={"per_page": 3}).configure(table)
    return render(request, template, {'rideform': rideform, 'table': table})

def ride_unique(request, unique_hash, template='main/account/quick_ride_view.html'):
    #ride = get_object_or_404(Ride, uuid=unique_hash)
    #import pdb;pdb.set_trace()
    ride = Ride.objects.select_related('driver').get(uuid=unique_hash)
    age = datetime.datetime.now().year - ride.driver.dob
    return render(request, template, {'ride': ride, 'age': age})


@csrf_exempt
def mail_from_postmark(request):
        if request.method == 'POST':
                json_data = request.body
                #body = json.loads(json_data)['HtmlBody']
                inbound = PostmarkInbound(json=json_data)
                if inbound.has_attachments():
                    attachments = inbound.attachments()
                    names = []
                    #absolue_uri = "<a href='"+request.build_absolute_uri(name1)+"'>" + name + "</a>"
                    for attachment in attachments:
                        name = attachment.name()
                        name1 = settings.MEDIA_URL + 'attachments/' + name
                        name2 = settings.MEDIA_ROOT + '/attachments/' + name                        
                        names.append(name1)
                        with open(name2,'w') as f:
                            myFile = File(f)
                            myFile.write(attachment.read())
                    mail = Inboundmail(html_body=inbound.text_body(), send_date=inbound.send_date(), subject=inbound.subject(), reply_to=inbound.reply_to(), sender=inbound.sender(), attachment=','.join(names))
                    #pdb.set_trace()
                else:
                    mail = Inboundmail(html_body=inbound.text_body(), send_date=inbound.send_date(), subject=inbound.subject(), reply_to=inbound.reply_to(), sender=inbound.sender())
                mail.save()
                return HttpResponse('OK')
        else:
                return HttpResponse('not OK')


@login_required
def profile(request, template='main/account/profile.html'):
    
    instance = request.user.driver.car if hasattr(request.user,'driver') and hasattr(request.user.driver,'car') else None
    userform   = UserForm(prefix='user', instance=request.user)
    if request.method == "POST":
        
        userform   = UserForm(request.POST, prefix='user', instance=request.user)
        if userform.is_valid():
            user = userform.save()

        messages.info(request, _("Your personal page has been updated!"))
    
        
    context = {"userform": userform}
    return render(request, template, context)


@login_required
def cars(request):
    instance = request.user.driver.car if hasattr(request.user,'driver') and hasattr(request.user.driver,'car') else None
    carform = CarForm(prefix='car', instance=instance, user=request.user)
    CarImageFormSet = inlineformset_factory(Car, CarImage, formset=BaseCarimageFormset, fields=('image',), max_num=6, extra=1,
                            widgets={'image': forms.FileInput()})
    formset = CarImageFormSet(instance=instance, user=request.user)
    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        formset       = CarImageFormSet(request.POST, request.FILES, instance=instance, user=request.user)
        if formset.is_valid():
            formset.save()
            
            messages.info(request, _("Successfully changed car images"))
            return redirect('cars')
    
        

    return render(request, 'main/account/cars.html', {'formset': formset, 'carform':carform})

@login_required
def additional_info(request, template='main/account/profile.html'):
    # if this is a POST request we need to process the form data
    #featured = request.FILES.get('driver-featured_image', None)
    #inst = request.user.driver if hasattr(request.user, 'driver') else None
    instance = request.user.driver if hasattr(request.user,'driver') else None
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        
        
        driverform = DriverForm(request.POST, instance=instance)

        # check whether it's valid:
        if driverform.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #data = driverform.cleaned_data
            #featured = data.get('featured_image')
            #import pdb;pdb.set_trace()
            if instance:
                #import pdb;pdb.set_trace()
                driverform.save()
            else:
                driver = driverform.save(commit=False)
                driver.user = request.user
                driver.save()
            
            messages.info(request, _("Your details have been saved!"))
            return redirect('profile')

    # if a GET (or any other method) we'll create a blank form
    else:
        driverform = DriverForm(instance=instance)

    return render(request, template, {'driverform': driverform})

    
def ajax_delete(request):
    if request.POST and request.is_ajax():
        Ride.objects.get(id=request.POST.get('id')).delete()
        return JsonResponse({'success': 1})
    return JsonResponse({'success': 0})


@csrf_exempt
@require_POST
def upd_pic(request, template='main/account/profile.html'):
    form = DriverForm(data=request.POST, files=request.FILES, instance=request.user.driver)
    #userform   = ProfileForm(prefix='user', instance=request.user)
    
    if form.is_valid():
        uploaded_file = form.save(commit=False)
        uploaded_file.featured_image=request.FILES.get('file')
        uploaded_file.save()
        #import pdb; pdb.set_trace()
        data = {
            'path': uploaded_file.featured_image.url,
        }
        return HttpResponse(json.dumps(data))
    return HttpResponseBadRequest(json.dumps({'errors': form.errors}))

def contact(request, template='main/pages/contact.html'):
    if request.method == "POST":
        
        form = ContactusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, _("We received your message and will get back to you soon, thanks!"))
            return redirect('home')
    else:
        form = ContactusForm()
    return render(request, template, {'form': form})

def about(request):
    return render(request, 'main/pages/about.html')

@login_required
def cardetails(request, template='main/account/cars.html'):
    fs_instance = request.user.driver.car if hasattr(request.user,'driver') and hasattr(request.user.driver,'car') else None
    CarImageFormSet = inlineformset_factory(Car, CarImage, formset=BaseCarimageFormset, fields=('image',), max_num=6, extra=1,
                            widgets={'image': forms.FileInput()})
    formset = CarImageFormSet(instance=fs_instance, user=request.user)
    instance = request.user.driver.car if hasattr(request.user.driver,'car') else None
    carform = CarForm(prefix='car', instance=instance, user=request.user)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        
        
        carform = CarForm(request.POST, prefix='car', instance=instance, user=request.user)

        # check whether it's valid:
        if carform.is_valid():
            car = carform.save(commit=False)
            car.driver = request.user.driver
            #import pdb;pdb.set_trace()
            car.save()
            messages.info(request, _("Your car details have been saved!"))
            return redirect('cars')
        
    userform   = ProfileForm(prefix='user', instance=request.user)
    return render(request, template, {'carform': carform, 'formset': formset})