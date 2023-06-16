from django.urls import path
from rest_framework.routers import DefaultRouter

from shop.views import OrderView, ColorView, CarModelView, CarBrandView, ColorInformView, BrandInformView

router = DefaultRouter()
router.register('brand', CarBrandView)
router.register('model', CarModelView)
router.register('color', ColorView)
router.register('order', OrderView)
router.register('color_inform', ColorInformView)
router.register('brand_inform', BrandInformView)

urlpatterns = router.urls
