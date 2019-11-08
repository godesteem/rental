from rest_framework import routers

from shop.views import OrderViewSet, ProductViewSet
from warehouse.views.warehouse import WarehouseItemViewSet

router = routers.SimpleRouter()
router.register(r'warehouse-items', WarehouseItemViewSet, basename='warehouse-items')
urlpatterns = router.urls
