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
# path('edit_profile/<int:user_id>', views.edit_profile, name = 'edit_profile'),
# path('view_myprofile/<int:user_id>', views.view_myprofile, name = 'view_myprofile'),
path('view_profile/<int:user_id>', views.view_profile, name = 'view_profile'),
]