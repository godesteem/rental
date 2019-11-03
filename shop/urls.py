from rest_framework import routers

from shop.views import OrderViewSet, ProductViewSet

router = routers.SimpleRouter()
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'products', ProductViewSet, basename='products')
urlpatterns = router.urls
