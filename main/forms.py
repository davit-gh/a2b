#!/usr/bin/env python
# -*- coding: utf-8 -*-

from main.models import City, Ride, Contactus, UserSearch, Driver, Image
from django.forms import ModelForm, Textarea
from django import forms
from django.utils.translation import ugettext as _
from functools import partial

# Form Fields
from django.utils import timezone
from datetimewidget.widgets import DateTimeWidget, TimeWidget, DateWidget
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext
from django.contrib.auth import authenticate
from django.utils.encoding import smart_text
from django.core.exceptions import ObjectDoesNotExist
import unicodedata, re, uuid
from ajax_upload.widgets import AjaxClearableFileInput

class UserSearchForm(ModelForm):
	
     
	fromwhere   = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Բոլորը", to_field_name="name_hy", required=False)
	towhere 	= forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Բոլորը", to_field_name="name_hy", required=False)
	leavedate   = forms.DateField(widget=DateWidget(options={'startDate':'+0d', 'format': 'dd-mm-yyyy'}), input_formats=['%d-%m-%Y','%d/%m/%Y'], required=False)
	class Meta:
 		model = UserSearch
		fields = ['fromwhere', 'towhere', 'leavedate']

	
		
class RideAdminForm(ModelForm):
    fromwhere   = forms.ModelChoiceField(label=u"Որտեղի՞ց", queryset=City.objects.all(), to_field_name="name_hy", required=True)
    towhere 	= forms.ModelChoiceField(label=u"Ու՞ր", queryset=City.objects.all(), to_field_name="name_hy", required=True)
    leavedate   = forms.CharField(label=u"Ամսաթիվ", widget=DateWidget(attrs={'id':"id_source"}, options={'startDate':'+0d'}), required=True)
    starttime   = forms.CharField(label=u"Ժամ", widget=TimeWidget(), required=True)
    class Meta:
        model = Ride
        exclude = ['endtime', 'driver', 'uuid']
        labels = {
            'passenger_number': u"Ազատ տեղերի քանակ", 
            'price': u"Գին"
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(RideAdminForm, self).__init__(*args, **kwargs)

    def clean_starttime(self):
        st = self.cleaned_data['starttime']
        if not st:
            raise forms.ValidationError('Նշեք ժամը, խնդրեմ')
        return st

    def clean_leavedate(self):
        leave_date = datetime.strptime(self.cleaned_data["leavedate"],'%d/%m/%Y')
        return leave_date

    def clean(self):
        if not self.user.driver.mobile:
            raise forms.ValidationError('mobile', code='mobile_error')
    
class ContactusForm(ModelForm):
	class Meta:
		model = Contactus
		fields = ['name', 'email', 'message']




class LoginForm(forms.Form):
    """
    Fields for login.
    """
    username = forms.CharField(label=u"Մուտքանուն")
    password = forms.CharField(label=u"Գաղտնաբառ",
                               widget=forms.PasswordInput(render_value=False))

    def clean(self):
        """
        Authenticate the given username/email and password. If the fields
        are valid, store the authenticated user for returning via save().
        """
        
        username = self.cleaned_data.get("username")
        u = User.objects.get(email=username)
        username = u.username
        password = self.cleaned_data.get("password")
        self._user = authenticate(username=username, password=password)
        if self._user is None:
            raise forms.ValidationError(
                             ugettext(u"Սխալ Էլ․ հասցե կամ գաղտնաբառ"))
        elif not self._user.is_active:
            raise forms.ValidationError(ugettext(u"Ձեր անձնական էջն ակտիվ չէ։"), code='inactive')
        return self.cleaned_data

    def save(self):
        """
        Just return the authenticated user - used for logging in.
        """
        return getattr(self, "_user", None)


class CarImageForm(forms.Form):
    image = forms.ImageField(required=False)

CHOICES=[('Արական','Արական'),
         ('Իգական','Իգական')]

BIRTH_YEAR_CHOICES = map(lambda x: (str(x),str(x)), range(1970,1992))
MOBILE_PREFIXES = [('055', '055'), ('095', '095'), ('043', '043'), ('077', '077'), ('093', '093'), ('094', '094'), ('098', '098'), ('091', '091'), ('099', '099')]

class DriverForm(forms.ModelForm):
    mobile_prefix  = forms.ChoiceField(choices=MOBILE_PREFIXES, required=False)
    mobile         = forms.CharField(label=u"Բջջային", required=False)
    sex            = forms.ChoiceField(label=u"Սեռ", choices=CHOICES, widget=forms.RadioSelect(), initial='Արական', required=False)
    featured_image = forms.ImageField(label=u"Իմ նկարը", widget=AjaxClearableFileInput(), required=False)
    dob            = forms.ChoiceField(label=u"Ծննդյան տարեթիվ", choices=BIRTH_YEAR_CHOICES, initial='1980', required=False)
    image_path     = forms.CharField(max_length=255, widget=forms.HiddenInput(), required=False)
    delete_image   = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Driver
        exclude = ['user', 'licence_plate' ]

    def clean_featured_image(self):
        pass
        #import pdb; pdb.set_trace()
        #img = Image.objects.create(image=self.files['file'])
        #data = self.cleaned_data['featured_image']
        # Change the name of the file to something unguessable
        # Construct the new name as <unique-hex>-<original>.<ext>
        #data.name = u'%s-%s' % (uuid.uuid4().hex, data.name)
        #return img
    #def __init__(self, *args, **kwargs):
        #self.user = kwargs.pop('user')
        #u = User.objects.get(id=self.user.id)
    #    super(DriverForm, self).__init__(*args, **kwargs)
    #    if hasattr(self.user, 'driver'):
    #        self.initial['mobile_prefix'] = self.user.driver.mobile_prefix
    #        self.initial['mobile'] = self.user.driver.mobile
    #        self.initial['dob'] = self.user.driver.dob
    #        self.initial['sex'] = self.user.driver.sex
        

    

class ProfileForm(forms.ModelForm):
    
    """
    ModelForm for auth.User - used for signup and profile update.
    If a Profile model is defined via ``AUTH_PROFILE_MODULE``, its
    fields are injected into the form.
    """
    #mobile          = forms.CharField(label=u"Բջջային",)
    #featured_image  = forms.ImageField(label=u"Գլխավոր նկար", required=True, widget=forms.FileInput)
    #gender          = forms.ChoiceField(label=u"Սեռ", choices=CHOICES, widget=forms.RadioSelect(), initial='Արական')
    password1       = forms.CharField(label=u"Գաղտնաբառ",
                                widget=forms.PasswordInput(render_value=False))
    password2       = forms.CharField(label=u"Գաղտնաբառ (Կրկնել)",
                                widget=forms.PasswordInput(render_value=False))
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        labels = {
            'first_name': u'Անուն',
            'last_name': u'Ազգանուն',
            'email': u'Էլեկտրոնային հասցե',
        }
        

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self._signup = self.instance.id is None
        user_fields = User._meta.get_fields()
        #self.fields.pop('username')
        #user = kwargs.pop('instance', None)
        #if user:
        #    self.fields['mobile'].initial = user.driver.mobile
            #import pdb;pdb.set_trace()
        #    self.fields['featured_image'].initial = user.driver.featured_image
        
        
        for field in self.fields:
            # Make user fields required.
            if field in user_fields:
                self.fields[field].required = True
            # Disable auto-complete for password fields.
            # Password isn't required for profile update.
            if field.startswith("password"):
                self.fields[field].widget.attrs["autocomplete"] = "off"
                self.fields[field].widget.attrs.pop("required", "")
                if not self._signup:
                    self.fields[field].required = False
                    if field == "password1":
                        self.fields[field].help_text = ugettext(
                        u"Թողեք դատարկ, եթե չեք ուզում փոխել ծածկագիրը։")
        

    

    def clean_password2(self):
        """
        Ensure the password fields are equal, and match the minimum
        length defined by ``ACCOUNTS_MIN_PASSWORD_LENGTH``.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1:
            errors = []
            if password1 != password2:
                errors.append(ugettext("Ծածկագրերը չեն համընկնում։"))
            if len(password1) < settings.ACCOUNTS_MIN_PASSWORD_LENGTH:
                errors.append(
                        ugettext("Ծածկագիրը պետք է լինի առնվազն %s սիմվոլ") %
                        settings.ACCOUNTS_MIN_PASSWORD_LENGTH)
            if errors:
                self._errors["password1"] = self.error_class(errors)
        return password2

    def clean_email(self):
        """
        Ensure the email address is not already registered.
        """
        email = self.cleaned_data.get("email")
        qs = User.objects.exclude(id=self.instance.id).filter(email=email)
        if len(qs) == 0:
            return email
        raise forms.ValidationError(
                                ugettext(u"Այս էլ․ հասցեն արդեն գրանցված է։"))


    def save(self, *args, **kwargs):
        """
        Create the new user. If no username is supplied (may be hidden
        via ``ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS`` or
        ``ACCOUNTS_NO_USERNAME``), we generate a unique username, so
        that if profile pages are enabled, we still have something to
        use as the profile's slug.
        """
        #import pdb;pdb.set_trace()
        kwargs["commit"] = False
        user = super(ProfileForm, self).save(*args, **kwargs)
        try:
            username = self.cleaned_data["username"]
        except KeyError:
            if not self.instance.username:
                username = self.cleaned_data["email"].split("@")[0]
                qs = User.objects.exclude(id=self.instance.id)
                user.username = unique_slug(qs, "username", slugify_unicode(username))
            else:
                username = self.instance.username
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        elif self._signup:
            try:
                user.set_unusable_password()
            except AttributeError:
                # This could happen if using a custom user model that
                # doesn't inherit from Django's AbstractBaseUser.
                pass
        user.save()

        user = authenticate(username=username, password=password)
        return user

    def get_profile_fields_form(self):
        return ProfileFieldsForm

def unique_slug(queryset, slug_field, slug):
    """
    Ensures a slug is unique for the given queryset, appending
    an integer to its end until the slug is unique.
    """
    i = 0
    while True:
        if i > 0:
            if i > 1:
                slug = slug.rsplit("-", 1)[0]
            slug = "%s-%s" % (slug, i)
        try:
            queryset.get(**{slug_field: slug})
        except ObjectDoesNotExist:
            break
        i += 1
    return slug


def slugify_unicode(s):
    """
    Replacement for Django's slugify which allows unicode chars in
    slugs, for URLs in Chinese, Russian, etc.
    Adopted from https://github.com/mozilla/unicode-slugify/
    """
    chars = []
    for char in smart_text(s):
        cat = unicodedata.category(char)[0]
        if cat in "LN" or char in "-_~":
            chars.append(char)
        elif cat == "Z":
            chars.append(" ")
    return re.sub("[-\s]+", "-", "".join(chars).strip()).lower()
