from django.shortcuts import render
from main.models import Driver
from main.forms import RidesearchForm
# Create your views here.
def index(request):
	drivers = Driver.objects.all()
	return render(request, "main/base.html", {'drivers': drivers})

def ridesearch(request):
	if request.method == 'POST':
		items = PortfolioItem.objects.filter(categories__slug=request.POST['towhere'])
		form = RidesearchForm(request.POST)
		if form.is_valid():
			form.save()
	else:
		form = RidesearchForm()
		items = PortfolioItem.objects.all()
	#pdb.set_trace()
	return render(request, 'main/pages/index.html', {'items': items})