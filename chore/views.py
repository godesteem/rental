from django.db.models import F, Func
from django.http import JsonResponse
from django.shortcuts import render

from chore.models import RentalPeriod
from chore.serializers import RentalPeriodSerializer


def get_data(request):
    rental_periods = RentalPeriod.objects.all().order_by('start_datetime')
    return JsonResponse(RentalPeriodSerializer(rental_periods, many=True).data, safe=False)


def visualisation(request):
    rental_periods = RentalPeriod.objects.all().order_by('start_datetime').annotate(
        duration=Func(F('end_datetime'), F('start_datetime'), function='age')
    )
    rental_periods = [{'id': i.id, 'start_datetime': i.start_datetime, 'end_datetime': i.end_datetime, 'duration': i.duration.days + 1} for i in rental_periods]
    return render(request, 'chore/rental_periods/rental_period_visualisation.html', {'rental_periods': rental_periods})
