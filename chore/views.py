import re

from django.http import JsonResponse
from django.shortcuts import render

from chore.models import RentalPeriod
from chore.serializers import RentalPeriodSerializer
from shop.models import Order, OrderItem
from shop.serializers import OrderSerializer


def get_data(request):
    rental_periods = RentalPeriod.objects.all().order_by('start_datetime')
    return JsonResponse(RentalPeriodSerializer(
        rental_periods, many=True
    ).data, safe=False)


def visualisation(request):
    view = request.GET.get('view')
    data = {}
    if view:
        if re.match(r'.*(rental-periods).*', view):
            rental_periods = RentalPeriod.objects.all(

            ).order_by('start_datetime')
            rental_periods = [{
                'id': i.id,
                'start_datetime': i.start_datetime,
                'end_datetime': i.end_datetime,
                'duration': i.duration,
            } for i in rental_periods]
            data.update({'rental_periods': rental_periods})
        if re.match(r'.*(orders).*', view):
            orders = Order.objects.all().order_by(
                'rental_period__start_datetime'
            )
            data.update({'orders': OrderSerializer(orders, many=True).data})
        if re.match(r'.*(products).*', view):
            products = OrderItem.objects.all().order_by(
                'product__id', 'order__rental_period__start_datetime'
            )
            products = [{
                'id': i.product.id,
                'start_datetime': i.order.rental_period.start_datetime,
                'end_datetime': i.order.rental_period.end_datetime,
                'product': i.product.name,
            } for i in products]
            data.update({'products': products})
    return render(
        request,
        'chore/rental_periods/rental_period_visualisation.html',
        data
    )


def management(request):
    return render(request, 'chore/index.html')
