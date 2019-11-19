from rest_framework import routers

from warehouse.views.storage import StorageUnitViewSet, StorageUnitComponentViewSet
from warehouse.views.warehouse import WarehouseItemViewSet, WarehouseComponentViewSet

router = routers.SimpleRouter()
router.register(r'warehouse-items', WarehouseItemViewSet,
                basename='warehouse-items')
router.register(r'warehouse-components', WarehouseComponentViewSet,
                basename='warehouse-components')
router.register(r'storage-units', StorageUnitViewSet,
                basename='storage-units')
router.register(r'storage-unit-components', StorageUnitComponentViewSet,
                basename='storage-unit-components')
urlpatterns = router.urls
