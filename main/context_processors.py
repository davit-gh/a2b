from main.forms import DriverForm

def driverimage(request):
	
	instance = request.user.driver if hasattr(request.user,'driver') else None
	driverform = DriverForm(prefix='driver', instance=instance)
	return {'driverform': driverform}
	