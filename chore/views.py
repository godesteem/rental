from django.http import JsonResponse
from django.shortcuts import render

from chore.models import RentalPeriod
from chore.serializers import RentalPeriodSerializer


def get_data(request):
    rental_periods = RentalPeriod.objects.all()
    return JsonResponse(RentalPeriodSerializer(rental_periods, many=True).data, safe=False)


def visualisation(request):
    return render(request, 'chore/rental_periods/rental_period_visualisation.html')
