from django.shortcuts import render
from django.http import HttpResponse
from main.forms import RidesearchForm
from main.models import PortfolioItem
import pdb
# Create your views here.
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
	return render(request, 'pages/index.html', {'items': items})

