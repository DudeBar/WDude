from django.contrib import admin
from website.models import FbAppAccount


class FbAppAccountAdmin(admin.ModelAdmin):
    pass
admin.site.register(FbAppAccount, FbAppAccountAdmin)
