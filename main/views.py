# coding: utf-8
from django.shortcuts import render, redirect
from main.models import Ride, Driver, DriverImage, Image, City
from main.tables import RideTable
from main.forms import UserSearchForm, ContactusForm, LoginForm, ProfileForm, RideAdminForm, CarImageForm, AddInfoForm
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_tables2   import RequestConfig
import json, pdb, datetime
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
import json
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
        form = ContactusForm(request.POST)
        if not form.has_changed(): form = ContactusForm()
        if form.is_valid():
	    form.save()
	    form = ContactusForm()
        post_dict = request.POST
        if not post_dict.get('fromwhere') and not post_dict.get('towhere'):
            rides = Ride.objects.all()
        else: 
            if post_dict.get('leavedate', None):
                fromwhere = City.objects.get(name_en=post_dict['fromwhere'])
                towhere   = City.objects.get(name_en=post_dict['towhere'])
                d = datetime.datetime.strptime(post_dict['leavedate'], '%d/%m/%Y')
                rides = Ride.objects.filter(fromwhere=fromwhere, towhere=towhere, 
                                            leavedate__year=d.year, leavedate__month=d.month, leavedate__day=d.day)
            else:
                rides = Ride.objects.filter(fromwhere=post_dict['fromwhere'], towhere=post_dict['towhere'])

    else:
	form = ContactusForm(request.POST)
	rides = Ride.objects.all()
		#items = PortfolioItem.objects.all()
    table = RideTable(rides)
    RequestConfig(request, paginate={"per_page": 3}).configure(table)
    loginform = LoginForm(prefix="login")
    return render(request, 'main/pages/search.html', {'table': table, 'form':form, 'loginform':loginform})

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
    DriverImageFormSet = formset_factory(CarImageForm, max_num=6)
    signup_form = ProfileForm()
    formset = DriverImageFormSet
    if request.method == "POST":
        #import pdb;pdb.set_trace()
        login_form = LoginForm(request.POST, prefix="login")
        signup_form = ProfileForm(request.POST, request.FILES)
        
        if not login_form.has_changed() and not request.POST.get("from_popup",False): login_form = LoginForm(prefix="login")
        if not signup_form.has_changed(): signup_form = ProfileForm()
        
        if login_form.is_valid():
            authenticated_user = login_form.save()
            messages.info(request, "Successfully logged in")
            auth_login(request, authenticated_user)
            
            return redirect('/')

        if signup_form.has_changed() and signup_form.is_valid():
            formset = DriverImageFormSet(request.POST, request.FILES)
            new_user = signup_form.save()
            #import pdb;pdb.set_trace()
            f_img = Image.objects.create(image=request.FILES.get('featured_image'))
            driver = Driver.objects.create(user=new_user, mobile=request.POST.get('mobile',None), featured_image=f_img)#set mobile and featured image
            
            
            if formset.is_valid():
                for form in formset: 
                    cd = form.cleaned_data
                    if cd:
                        dci = DriverImage(driver=driver, image=cd.get('image'))
                        dci.save()

            
            messages.info(request, "Successfully signed up")
            auth_login(request, new_user)
            return redirect("/")
    #import pdb;pdb.set_trace()
    context = {"login_form": login_form, "signup_form": signup_form, "formset": formset}
    return render(request, template, context)

from django.forms import BaseInlineFormSet

class CustomInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(CustomInlineFormSet, self).__init__(*args, **kwargs)
        #for form in self.forms:
            #import pdb;pdb.set_trace()
        imgs = User.objects.get(username=self.forms[0].data['username']).driver.imgs.all()
        im = map(lambda x: {'image':x.image.image}, imgs)
        for subf, data in zip(self.forms, im): subf.initial=data
        #form.initial = {'image': form.instance.image.image}
    
@login_required
def profile_update(request, template="main/pages/account_profile_update.html"):
    """
    Profile update form.
    """
    
    profile_form = ProfileForm
    DriverImageFormSet = inlineformset_factory(Driver, DriverImage, fields=('image',), max_num=6, extra=0,
                            widgets={'image': forms.FileInput()})
    
    driver = Driver.objects.get(user=request.user)
   
    if request.method == "POST":
        form = profile_form(request.POST, request.FILES or None,
                            instance=request.user)
        formset = DriverImageFormSet(request.POST, request.FILES, instance=driver)
        
        #import pdb;pdb.set_trace()
        featured = request.FILES.get('featured_image', None)
        if form.is_valid() and formset.is_valid():
            #import pdb;pdb.set_trace()
            driver.mobile = request.POST.get('mobile', None)
            if featured:
                img = Image.objects.get(id=driver.featured_image.id)
                img.image = featured
                img.save()
            #driver.images = 
            driver.save()
            form.save()
            if formset.has_changed(): 
                formset.save()
            messages.info(request, _("Profile updated"))
            return redirect("/")
    else:
        form = profile_form(instance=request.user)#;
        formset = DriverImageFormSet(instance=driver)
    context = {"form": form, "title": _("Update Profile"), "formset": formset}
    return render(request, template, context)


@login_required
def rides(request, template="main/pages/ride.html"):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RideAdminForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            ride = form.save(commit=False)
            ride.driver = request.user.driver
            ride.starttime = datetime.datetime.now()
            ride.save()
            messages.info(request, "Երթուղին ավելացված է")
            return redirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RideAdminForm()

    return render(request, template, {'form': form})


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


def add_info(request, template='main/pages/add_info.html'):
    
    DriverImageFormSet = formset_factory(CarImageForm, max_num=6)
    
     
    if request.method == "POST":
        form = AddInfoForm(request.POST, request.FILES)
        formset = DriverImageFormSet(request.POST, request.FILES)
        
        #import pdb;pdb.set_trace()
        featured = request.FILES.get('featured_image', None)
        if form.is_valid() and formset.is_valid():
            #import pdb;pdb.set_trace()
            
            if featured:
                img = Image.objects.create(image=featured)
                
            #driver.images = 
            driver = Driver(mobile=form.cleaned_data['mobile'], featured_image=img, user=request.user)
            driver.save()
            for form in formset: 
                cd = form.cleaned_data
                if cd:
                    dci = DriverImage(driver=driver, image=cd.get('image'))
                    dci.save()
            messages.info(request, _("Profile updated"))
            return redirect("/")
    else:
        form = AddInfoForm()
        formset = DriverImageFormSet()
    context = {"form": form, "formset": formset}
    return render(request, template, context)
