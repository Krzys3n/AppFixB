from django.urls import path
from . import views

urlpatterns = [
# Strona główna.
path('', views.index, name='index'),
path('apps/', views.apps, name='apps'),
path('apps/(<int:app_id>)/', views.app, name='app'),
path('new_app/', views.new_app, name='new_app'),
path('new_report/(<int:app_id>)', views.new_report, name='new_report'),
path('edit_report/<int:report_id>/', views.edit_report,name='edit_report'),
path('edit_profile/', views.edit_profile, name = 'edit_profile'),
path('view_profile/<int:user_id>', views.view_profile, name = 'view_profile'),
path('company/', views.company, name = 'company'),
path('new_company/', views.new_company, name = 'new_company'),
path('company_memebrs', views.company_members, name = 'company_members'),
path('company_invitations', views.company_invitations, name = 'company_invitations')

]