#!/usr/bin/env python
# -*- coding: utf-8 -*-

from main.models import City, Ride, Contactus, UserSearch
from django.forms import ModelForm, Textarea
from django import forms
from django.utils.translation import ugettext as _
from functools import partial
DateInput = partial(forms.DateInput, )

# Form Fields
from django.utils import timezone
from datetimewidget.widgets import DateTimeWidget
from datetimewidget.widgets import DateWidget
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext
from django.contrib.auth import authenticate



class UserSearchForm(ModelForm):
	
     
	fromwhere   = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Բոլորը", to_field_name="name_hy", widget=forms.Select(attrs={"onChange":'sourcefilter(this)'}))
	towhere 	= forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Բոլորը", to_field_name="name_hy", widget=forms.Select(attrs={"onChange":'destfilter(this)'}))
	leavedate   = forms.CharField(widget=DateWidget(attrs={'id':"id_source"}, options={'startDate':'+1d'}))
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
	class Meta:
 		model = Ride
		fields = ['fromwhere', 'towhere', 'leavedate', 'endtime', 'howmuch', 'driver']
		

class ContactusForm(ModelForm):
	class Meta:
		model = Contactus
		fields = ['name', 'email', 'message']


class Html5Mixin(object):
    """
    Mixin for form classes. Adds HTML5 features to forms for client
    side validation by the browser, like a "required" attribute and
    "email" and "url" input types.
    """

    def __init__(self, *args, **kwargs):
        super(Html5Mixin, self).__init__(*args, **kwargs)
        if hasattr(self, "fields"):
            # Autofocus first field
            first_field = next(iter(self.fields.values()))
            first_field.widget.attrs["autofocus"] = ""

            for name, field in self.fields.items():
                if settings.FORMS_USE_HTML5:
                    if isinstance(field, forms.EmailField):
                        self.fields[name].widget.input_type = "email"
                    elif isinstance(field, forms.URLField):
                        self.fields[name].widget.input_type = "url"
                if field.required:
                    self.fields[name].widget.attrs["required"] = ""


class LoginForm(Html5Mixin, forms.Form):
    """
    Fields for login.
    """
    username = forms.CharField(label="Login")
    password = forms.CharField(label="Password",
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
                             ugettext("Invalid username/email and password"))
        elif not self._user.is_active:
            raise forms.ValidationError(ugettext("Your account is inactive"))
        return self.cleaned_data

    def save(self):
        """
        Just return the authenticated user - used for logging in.
        """
        return getattr(self, "_user", None)


class ProfileForm(Html5Mixin, forms.ModelForm):
    """
    ModelForm for auth.User - used for signup and profile update.
    If a Profile model is defined via ``AUTH_PROFILE_MODULE``, its
    fields are injected into the form.
    """

    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label="Password (again)",
                                widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")
        

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self._signup = self.instance.id is None
        user_fields = User._meta.get_all_field_names()
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