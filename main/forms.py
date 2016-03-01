#!/usr/bin/env python
# -*- coding: utf-8 -*-

from main.models import City, Ride, Contactus, UserSearch, Driver
from django.forms import ModelForm, Textarea
from django import forms
from django.utils.translation import ugettext as _
from functools import partial
DateInput = partial(forms.DateInput, )

# Form Fields
from django.utils import timezone
from datetimewidget.widgets import DateTimeWidget, TimeWidget, DateWidget
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext
from django.contrib.auth import authenticate


class UserSearchForm(ModelForm):
	
     
	fromwhere   = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Բոլորը", to_field_name="name_hy", widget=forms.Select(attrs={"onChange":'sourcefilter(this)'}))
	towhere 	= forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Բոլորը", to_field_name="name_hy", widget=forms.Select(attrs={"onChange":'destfilter(this)'}))
	leavedate   = forms.CharField(widget=DateWidget(attrs={'id':"id_source"}, options={'startDate':'+0d'}))
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
    leavedate   = forms.CharField(widget=DateWidget(attrs={'id':"id_source"}, options={'startDate':'+0d'}))
    starttime   = forms.CharField(widget=TimeWidget())
    class Meta:
        model = Ride
        fields = ['fromwhere', 'towhere', 'leavedate', 'starttime', 'passenger_number', 'price']
	
    def clean_leavedate(self):
        leave_datetime = self.cleaned_data["leavedate"]
        leave_date = datetime.strptime(leave_datetime,'%d/%m/%Y')
        return leave_date.strftime('%Y-%m-%d')

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
        password = self.cleaned_data.get("password")
        self._user = authenticate(username=username, password=password)
        if self._user is None:
            raise forms.ValidationError(
                             ugettext(u"Սխալ Էլ․ հասցե/մուտքանուն կամ գաղտնաբառ"))
        elif not self._user.is_active:
            raise forms.ValidationError(ugettext("Your account is inactive"))
        return self.cleaned_data

    def save(self):
        """
        Just return the authenticated user - used for logging in.
        """
        return getattr(self, "_user", None)


class CarImageForm(forms.Form):
    image = forms.ImageField(required=False)


CHOICES=[('Կին','Կին'),
         ('Տղամարդ','Տղամարդ')]

class AddInfoForm(forms.Form):
    mobile         = forms.CharField(label=u"Բջջային",)
    gender         = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    featured_image = forms.ImageField(required=True)

class ProfileForm(forms.ModelForm):
    
    """
    ModelForm for auth.User - used for signup and profile update.
    If a Profile model is defined via ``AUTH_PROFILE_MODULE``, its
    fields are injected into the form.
    """
    mobile          = forms.CharField(label=u"Բջջային",)
    featured_image  = forms.ImageField(label=u"Գլխավոր նկար", required=True, widget=forms.FileInput)
    password1       = forms.CharField(label=u"Գաղտնաբառ",
                                widget=forms.PasswordInput(render_value=False))
    password2       = forms.CharField(label=u"Գաղտնաբառ (Կրկնել)",
                                widget=forms.PasswordInput(render_value=False))
    
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")
        labels = {
            'first_name': u'Անուն',
            'last_name': u'Ազգանուն',
            'email': u'Էլեկտրոնային հասցե',
            'username': u'Մուտքանուն',
        }
        

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self._signup = self.instance.id is None
        user_fields = User._meta.get_fields()
        user = kwargs.pop('instance', None)
        if user:
            self.fields['mobile'].initial = user.driver.mobile
            #import pdb;pdb.set_trace()
            self.fields['featured_image'].initial = user.driver.featured_image
        
        try:
            self.fields["username"].help_text = ugettext(
                        "Only letters, numbers, dashes or underscores please")
            
        except KeyError:
            pass
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
                        "Leave blank unless you want to change your password")
        

    def clean_username(self):
        """
        Ensure the username doesn't exist or contain invalid chars.
        We limit it to slugifiable chars since it's used as the slug
        for the user's profile view.
        """
        username = self.cleaned_data.get("username")
        
        lookup = {"username__iexact": username}
        try:
            User.objects.exclude(id=self.instance.id).get(**lookup)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
                            ugettext("This username is already registered"))

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
                errors.append(ugettext("Passwords do not match"))
            if len(password1) < settings.ACCOUNTS_MIN_PASSWORD_LENGTH:
                errors.append(
                        ugettext("Password must be at least %s characters") %
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
                                ugettext("This email is already registered"))

    def save(self, *args, **kwargs):
        """
        Create the new user. If no username is supplied (may be hidden
        via ``ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS`` or
        ``ACCOUNTS_NO_USERNAME``), we generate a unique username, so
        that if profile pages are enabled, we still have something to
        use as the profile's slug.
        """

        kwargs["commit"] = False
        user = super(ProfileForm, self).save(*args, **kwargs)
        try:
            username = self.cleaned_data["username"]
        except KeyError:
            if not self.instance.username:
                username = self.cleaned_data["email"].split("@")[0]
                qs = User.objects.exclude(id=self.instance.id)
                user.username = unique_slug(qs, "username", slugify(username))
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

        
        if self._signup:
            if (settings.ACCOUNTS_VERIFICATION_REQUIRED or
                settings.ACCOUNTS_APPROVAL_REQUIRED):
                user.is_active = False
                user.save()
            else:
                
                user = authenticate(username=username, password=password)
        return user

    def get_profile_fields_form(self):
        return ProfileFieldsForm