from django.contrib import admin
from main.models import Driver, Ride, City, Contactus, CarImage
from main.forms import RideAdminForm
from main.models import Inboundmail

class RideAdmin(admin.ModelAdmin):
	"""docstring for RideAdmin"""
	
	form = RideAdminForm

class RideInline(admin.TabularInline):
	model=Ride
	extra = 1
	max_num = 333
	form = RideAdminForm

# class DriverCarImageInline(admin.TabularInline):
# 	model=CarImage
# 	extra = 1
# 	max_num = 333

class DriverAdmin(admin.ModelAdmin):
	inlines=(RideInline, )#DriverCarImageInline, )


class InboundmailAdmin(admin.ModelAdmin):
        list_display=('send_date', 'subject', 'html_body', 'reply_to', 'sender', 'htmlify')

admin.site.register(Inboundmail, InboundmailAdmin)
admin.site.register(Ride, RideAdmin)
admin.site.register(City)
admin.site.register(Contactus)
admin.site.register(Driver, DriverAdmin)