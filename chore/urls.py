from django.urls import path, re_path

from chore import views

urlpatterns = [
    path('visualisation/', views.visualisation, name='visualization'),
    path('rental-periods/visualization/get-data/',
         views.get_data,
         name='rental-period-visualization-get_data'),
    re_path(r'^.*', views.management, name='management'),
]
