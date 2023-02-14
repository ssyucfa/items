from django.contrib import admin

from .models import Discount, Item, Order, Tax

admin.site.register(Order, admin.ModelAdmin)
admin.site.register(Discount, admin.ModelAdmin)
admin.site.register(Item, admin.ModelAdmin)
admin.site.register(Tax, admin.ModelAdmin)
