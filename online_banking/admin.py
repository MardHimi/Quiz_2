from django.contrib import admin
from .models import User_profile, Account, debt
# Register your models here.

admin.site.register(User_profile)
admin.site.register(Account)
admin.site.register(debt)
