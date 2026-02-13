from django.urls import path
from . import views


urlpatterns = [

    path('', views.home, name='home'),

    path('save-report/', views.save_report, name='save_report'),

]