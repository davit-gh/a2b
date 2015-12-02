from django.contrib import admin
from main.models import HomePage, Slide
from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin
from main.models import Portfolio, PortfolioItem, PortfolioItemImage, PortfolioItemCategory
#from main.models import Order
#from cartridge.shop.forms import ProductAdminForm

class SlideAdmin(TabularDynamicInlineAdmin):
	model=Slide


class HomePageAdmin(PageAdmin):
	inlines = [SlideAdmin,]


class PortfolioItemImageInline(TabularDynamicInlineAdmin):
	model=PortfolioItemImage

class PortfolioItemAdmin(PageAdmin):
	inlines=(PortfolioItemImageInline, )

#admin.site.register(Order,PageAdmin)
admin.site.register(HomePage,HomePageAdmin)
admin.site.register(Portfolio,PageAdmin)
admin.site.register(PortfolioItem,PortfolioItemAdmin)
admin.site.register(PortfolioItemCategory)
