from django.contrib import admin

from AppFixB1.models import User ,Company, UserCompany

# Register your models here.
admin.site.register(User)
admin.site.register(Company)
admin.site.register(UserCompany)