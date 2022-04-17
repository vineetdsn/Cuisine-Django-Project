from django.contrib import admin
from core.models import (Category, 
UserDetail,Item,Cart,Orders)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id","title","is_active","added_on"]

class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'sale_price','image']

class CartAdmin(admin.ModelAdmin):
	list_display = ['user', 'item','quantity','status']


class OrdersAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name','phone','city','total','status']
    list_filter = ['status']
    readonly_fields = ('user','address','city','phone','first_name','ip', 'last_name','phone','city','total')
    can_delete = False
    #inlines = [OrderProductline]

admin.site.register(Orders,OrdersAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(UserDetail)