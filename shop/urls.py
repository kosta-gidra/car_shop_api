from django.urls import path
from rest_framework.routers import DefaultRouter

from shop.views import OrderView, ColorView, CarModelView, CarBrandView, ColorInformView, BrandInformView

router = DefaultRouter()
router.register('brand', CarBrandView)
router.register('model', CarModelView)
router.register('color', ColorView)
router.register('order', OrderView)

urlpatterns = [
    path('color/inform/', ColorInformView.as_view(), name='color_inform'),
    path('brand/inform/', BrandInformView.as_view(), name='brand_inform'),
] + router.urls
