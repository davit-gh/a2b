from main.forms import DriverForm, LoginForm

def driverimage(request):
	loginform = LoginForm(prefix="login")
	instance = request.user.driver if hasattr(request.user,'driver') else None
	driverform = DriverForm(instance=instance)
	return {'loginform': loginform, 'driverform': driverform}
	