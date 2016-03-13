from main.forms import DriverForm

def driverimage(request):
	if request.user.is_authenticated() and not request.user.is_staff:
		driverform = DriverForm(prefix='driver', instance=request.user.driver)
		return {'driverform': driverform}
	return {}