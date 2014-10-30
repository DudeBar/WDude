from django.contrib import admin
from website.models import FbAppAccount, Customer, Product, Billing, Command, ProductQuantity, WheelCustomer, Commerces


class FbAppAccountAdmin(admin.ModelAdmin):
    pass

class CustomerAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    pass

class BillingAdmin(admin.ModelAdmin):
    pass

class CommandAdmin(admin.ModelAdmin):
    pass

class ProductQuantityAdmin(admin.ModelAdmin):
    pass

class WheelCustomerAdmin(admin.ModelAdmin):
    pass

class CommercesAdmin(admin.ModelAdmin):
    pass

admin.site.register(ProductQuantity, ProductQuantityAdmin)
admin.site.register(WheelCustomer, WheelCustomerAdmin)
admin.site.register(Command, CommandAdmin)
admin.site.register(Billing, BillingAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(FbAppAccount, FbAppAccountAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Commerces, CommercesAdmin)
