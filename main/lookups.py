from ajax_select import LookupChannel
from main.models import City
from django.db.models import Q
from django.utils.html import escape
class CityLookup(LookupChannel):

    model = City

    def get_query(self,q,request):
	return City.objects.filter(Q(name_en__icontains=q) | Q(name_hy__icontains=q))

    def check_auth(self, request):
            return True
  
    def get_result(self, obj):
        u""" result is the simple text that is the completion of what the person typed """
        return obj.name_hy

    def format_match(self, obj):
        """ (HTML) formatted item for display in the dropdown """
        return u"%s<div><i>%s</i></div>" % (escape(obj.name_en), escape(obj.name_hy))
        # return self.format_item_display(obj)

    def format_item_display(self, obj):
        """ (HTML) formatted item for displaying item in the selected deck area """
        return u"%s<div><i>%s</i></div>" % (escape(obj.name_en), escape(obj.name_hy))


class HayStreetLookup(LookupChannel):

    model = City

    def get_query(self,q,request):
	query = City.objects.filter(name_hy__icontains=q).order_by('name_hy')        
	return map(lambda x: x.name_hy, query)
