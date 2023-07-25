from django.contrib import admin


from django.shortcuts import render
from .models import App, Report, User, Company, UserCompany, Invitation


class ReportAdmin(admin.ModelAdmin):
    list_display = ('get_app_name','date_created' )

    def get_app_name(self, obj):
        return obj.reportId.appName if obj.reportId else ''

    get_app_name.short_description = 'App Name'
#
#
# admin.site.register(App, AppAdmin)
# admin.site.register(Report, ReportAdmin)



class ReportInline(admin.TabularInline):
    model = Report
    extra = 0

class AppAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ReportInline]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        app = self.get_object(request, object_id)
        extra_context['reports'] = app.report_set.all()  # Retrieve reports for the current app
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

admin.site.register(App, AppAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Invitation)