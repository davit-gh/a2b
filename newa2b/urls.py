"""newa2b URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from main import views
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url("^$", views.contactus, name="home"),
    url("^index/", views.index, name="index"),
    url(r'^getcar',  views.get_car_images, name='get_car_images'),
    url("^login$", views.login, name="login"),
    url("^logout$", views.logout, name="logout"),
    url("^signup$", views.signup, name="signup"),
    url("^update$", views.profile_update, name="profile_update"),
    url("^profile/home$", views.profile, name="profile"),
    url("^profile/info$", views.additional_info, name="info"),
    url("^profile/cars$", views.cars, name="cars"),
    url("^profile/rides$", views.rides, name="rides"),
    url(r"^mail", views.mail_from_postmark, name="postmark"),
    url(r'^accounts/', include('allauth.urls')),
    url("^ajax_delete$", views.ajax_delete, name="del-ride"),
    url(r'^ajax$', views.upd_pic, name='ajax-upload'),
    url(r'^about/', views.about, name='about'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^ride/(?P<unique_hash>[a-zA-Z0-9_]*)/$', views.ride_unique, name='runique'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^car/details', views.cardetails, name="cardetails")
]
