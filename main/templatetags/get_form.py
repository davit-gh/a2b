from mezzanine import template
from main.forms import RidesearchForm 
register = template.Library()
import pdb
@register.as_tag
def searchform(*args):
    #pdb.set_trace()    
    return RidesearchForm()
    