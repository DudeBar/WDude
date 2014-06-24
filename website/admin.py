from django.contrib import admin
from website.models import FbAppAccount, Customer, Product


class FbAppAccountAdmin(admin.ModelAdmin):
    pass

class CustomerAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(FbAppAccount, FbAppAccountAdmin)
admin.site.register(Customer, CustomerAdmin)
