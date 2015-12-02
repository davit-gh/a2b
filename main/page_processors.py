from mezzanine.pages.page_processors import processor_for
from main.models import PortfolioItem, HomePage, Portfolio
from mezzanine.forms.models import Form
import pdb
@processor_for(Form)
def home_processor(request, page):
    items = PortfolioItem.objects.published().prefetch_related('categories')
    items = items.filter(parent=Portfolio.objects.get(title="My portfolio"))
    #pdb.set_trace()
    return {'items': items}

