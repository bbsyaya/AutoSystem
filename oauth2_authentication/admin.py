from django.contrib import admin

# Register your models here.
from oauth2_authentication.models import CredentialsModel


class CredentialsAdmin(admin.ModelAdmin):
    pass


admin.site.register(CredentialsModel, CredentialsAdmin)