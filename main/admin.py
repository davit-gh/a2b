from django.contrib import admin
from main.models import Driver, Ride, City, Contactus, DriverCarImage, HowItWorks
from main.forms import RidesearchForm, RideAdminForm

class RideAdmin(admin.ModelAdmin):
	"""docstring for RideAdmin"""
	
	form = RideAdminForm

class RideInline(admin.TabularInline):
	model=Ride
	extra = 1
	max_num = 333
	form = RideAdminForm

class DriverCarImageInline(admin.TabularInline):
	model=DriverCarImage
	extra = 1
	max_num = 333

class DriverAdmin(admin.ModelAdmin):
	inlines=(DriverCarImageInline, RideInline, )


admin.site.register(Ride, RideAdmin)
admin.site.register(City)
admin.site.register(HowItWorks)
admin.site.register(Contactus)
admin.site.register(Driver, DriverAdmin)