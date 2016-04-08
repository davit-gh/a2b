#!/usr/bin/env python
# -*- coding: utf-8 -*-

from main.models import City, Ride, Contactus, UserSearch, Driver, Car
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
from django.utils.translation import ugettext, ugettext_lazy
from django.contrib.auth import authenticate
from django.utils.encoding import smart_text
from django.core.exceptions import ObjectDoesNotExist
import unicodedata, re, uuid
from ajax_upload.widgets import AjaxClearableFileInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field
from crispy_forms.bootstrap import StrictButton, PrependedText

class UserSearchForm(ModelForm):
	
     
	fromwhere   = forms.ModelChoiceField(queryset=City.objects.all(), empty_label=ugettext_lazy("All"), to_field_name="name_hy", required=False)
	towhere 	= forms.ModelChoiceField(queryset=City.objects.all(), empty_label=ugettext_lazy("All"), to_field_name="name_hy", required=False)
	leavedate   = forms.DateField(widget=DateWidget(options={'startDate':'+0d', 'format': 'dd-mm-yyyy', 'pickerPosition': 'top-right'}), input_formats=['%d-%m-%Y','%d/%m/%Y'], required=False)
	class Meta:
 		model = UserSearch
		fields = ['fromwhere', 'towhere', 'leavedate']

	
		
class RideAdminForm(ModelForm):
    fromwhere   = forms.ModelChoiceField(label=ugettext_lazy("From where"), queryset=City.objects.all(), to_field_name="name_hy", required=True)
    towhere 	= forms.ModelChoiceField(label=ugettext_lazy("To where"), queryset=City.objects.all(), to_field_name="name_hy", required=True)
    leavedate   = forms.CharField(label=ugettext_lazy("Date"), widget=DateWidget(attrs={'id':"id_source"}, options={'startDate':'+0d'}), required=True)
    starttime   = forms.CharField(label=ugettext_lazy("Time"), widget=TimeWidget(), required=True)
    class Meta:
        model = Ride
        exclude = ['endtime', 'driver', 'uuid']
        labels = {
            'passenger_number': ugettext_lazy("Free seats"), 
            'price': ugettext_lazy("Price")
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(RideAdminForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = 'rides'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-6'
        self.helper.field_class = 'col-xs-6'
        self.helper.layout = Layout(
            Field('fromwhere', required='required'),
            Field('towhere', required='required'),
            Field('leavedate', required='required'),
            Field('starttime', required='required'),
            Field('price', required='required'),
            'passenger_number',
            Div(
                Submit('submit', ugettext("Save"), css_class='btn btn-primary'),
                css_class='text-center',
                css_id='submit_btn'
            )
        )
    def clean_starttime(self):
        st = self.cleaned_data['starttime']
        if not st:
            raise forms.ValidationError(ugettext("Enter the time, please"))
        return st

    def clean_leavedate(self):
        leave_date = datetime.strptime(self.cleaned_data["leavedate"],'%d/%m/%Y')
        return leave_date

    def clean(self):
        if not hasattr(self.user, 'driver') or not self.user.driver.mobile:
            raise forms.ValidationError('mobile', code='mobile_error')
    
class ContactusForm(ModelForm):
	class Meta:
		model = Contactus
		fields = ['name', 'email', 'message']




class LoginForm(forms.Form):
    """
    Fields for login.
    """
    username = forms.EmailField(label=ugettext_lazy("Email"))
    password = forms.CharField(label=ugettext_lazy("Password"),
                               widget=forms.PasswordInput(render_value=False))
    #from_popup = forms.CharField()
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = 'signup'
        self.helper.layout = Layout(
            PrependedText('username', '@', placeholder=ugettext("Email, please")),
            PrependedText('password', '*', placeholder=ugettext("Password, please")),
            Field('from_popup', type="hidden"),
            Div(
                Submit('submit', ugettext("Login")),
                css_class='text-center',
                css_id='login_btn'
            )
        )

    def clean(self):
        """
        Authenticate the given username/email and password. If the fields
        are valid, store the authenticated user for returning via save().
        """
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("username")
        try:
           u = User.objects.get(email=email)
           self._user = authenticate(username=u.username, password=password)
        except ObjectDoesNotExist:
            raise forms.ValidationError(ugettext("Your email or password is wrong."), code='nonexistent')
        return self.cleaned_data

    def save(self):
        """
        Just return the authenticated user - used for logging in.
        """
        return getattr(self, "_user", None)


CHOICES=[('male', ugettext_lazy("Male")),
         ('female', ugettext_lazy("Female"))]

BIRTH_YEAR_CHOICES = map(lambda x: (str(x),str(x)), range(1970,1992))
MOBILE_PREFIXES = [('055', '055'), ('095', '095'), ('043', '043'), ('077', '077'), ('093', '093'), ('094', '094'), ('098', '098'), ('091', '091'), ('099', '099')]

class DriverForm(forms.ModelForm):
    mobile_prefix  = forms.ChoiceField(choices=MOBILE_PREFIXES, required=False)
    mobile         = forms.CharField(label=ugettext_lazy("Mobile"), required=False)
    sex            = forms.ChoiceField(label=ugettext_lazy("Gender"), choices=CHOICES, widget=forms.RadioSelect(), initial=ugettext_lazy("Male"), required=False)
    featured_image = forms.ImageField(label=ugettext_lazy("My photo"), widget=AjaxClearableFileInput(), required=False)
    dob            = forms.ChoiceField(label=ugettext_lazy("Birth year"), choices=BIRTH_YEAR_CHOICES, initial='1988', required=False)
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
        
class CarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CarForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = 'cardetails'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-6'
        self.helper.field_class = 'col-xs-6'
        self.helper.layout = Layout(
            Field('car_brand', required='required'),
            Field('licence_plate', required='required'),
            Div(
                Submit('submit', ugettext("Save")),
                css_class='text-center',
            )
        )
    class Meta:
        model = Car
        exclude = ['driver']

    def clean(self):
        if not hasattr(self.user, 'driver'):
            raise ValidationError(_("First fill in driver details, please."))

class ProfileForm(forms.ModelForm):
    
    """
    ModelForm for auth.User - used for signup and profile update.
    If a Profile model is defined via ``AUTH_PROFILE_MODULE``, its
    fields are injected into the form.
    """
    #mobile          = forms.CharField(label=u"Բջջային",)
    #featured_image  = forms.ImageField(label=u"Գլխավոր նկար", required=True, widget=forms.FileInput)
    #gender          = forms.ChoiceField(label=u"Սեռ", choices=CHOICES, widget=forms.RadioSelect(), initial='Արական')
    password1       = forms.CharField(label=ugettext_lazy("Password"),
                                widget=forms.PasswordInput(render_value=False), required=False)
    password2       = forms.CharField(label=ugettext_lazy("Password (again)"),
                                widget=forms.PasswordInput(render_value=False), required=False)
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        labels = {
            'first_name': ugettext_lazy("First name"),
            'last_name': ugettext_lazy("Last name"),
            'email': ugettext_lazy("Email"),
        }
        

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = 'profile'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-6'
        self.helper.field_class = 'col-xs-6'
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            Div(
                Submit('submit', ugettext("Save"), css_class='btn-primary'),
                css_class='text-center',
                css_id='submit_btn'
            )
        )
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
                errors.append(ugettext("Passwords are not the same"))
            if len(password1) < settings.ACCOUNTS_MIN_PASSWORD_LENGTH:
                errors.append(
                        ugettext("Password must contain at least %s symbols") %
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
                                ugettext("This email is already registered."))


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
