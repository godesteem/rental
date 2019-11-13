from django.urls import path

from chore import views

urlpatterns = [
    path('rental-periods/visualisation/', views.visualisation, name='rental-period-visualization'),
    path('rental-periods/visualization/get-data/', views.get_data, name='rental-period-visualization-get_data'),
]
