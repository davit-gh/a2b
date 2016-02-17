from django import template
from main.forms import UserSearchForm 
register = template.Library()
import pdb
@register.simple_tag
def searchform(*args):
    #pdb.set_trace()    
    return UserSearchForm()
    
@register.simple_tag
def get_contact_form(*args):
	return ContactusForm()