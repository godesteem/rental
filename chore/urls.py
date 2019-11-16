from django.urls import path

from chore import views

urlpatterns = [
    path('', views.management, name='management'),
    path('visualisation/', views.visualisation, name='visualization'),
    path('rental-periods/visualization/get-data/', views.get_data, name='rental-period-visualization-get_data'),
]
