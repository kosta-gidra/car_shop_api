from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from shop.models import CarBrand, CarModel, Color, Order
from shop.serializers import ColorSerializer, OrderSerializer, FullCarBrandSerializer, \
    FullOrderSerializer, CarModelSerializer, ColorWithCountSerializer, CarBrandWithCountSerializer


class OrderPagination(PageNumberPagination):
    """ Класс для пагинации страниц списка заказов"""
    page_size = 10


class CarBrandView(ModelViewSet):
    """
    Класс для работы с брендами автомобилей
    """
    queryset = CarBrand.objects.all()
    serializer_class = FullCarBrandSerializer


class CarModelView(ModelViewSet):
    """
    Класс для работы с моделями автомобилей
    """
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer


class ColorView(ModelViewSet):
    """
    Класс для работы с цветами
    """
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class OrderView(ModelViewSet):
    """
    Класс для работы с заказами
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['model__brand']
    ordering_fields = ['quantity']

    # заменил сериалайзер при отправке 'GET' запроса , чтобы получать расширенную информацию по заказам
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FullOrderSerializer
        else:
            assert self.serializer_class is not None, (
                    "'%s' should either include a `serializer_class` attribute, "
                    "or override the `get_serializer_class()` method."
                    % self.__class__.__name__
            )
            return self.serializer_class


class ColorInformView(ReadOnlyModelViewSet):
    """Класс для вывода списка цветов с указанием количества заказанных авто каждого цвета"""

    queryset = Color.objects.annotate(quantity=Sum('orders__quantity')).order_by('id')
    serializer_class = ColorWithCountSerializer


class BrandInformView(ReadOnlyModelViewSet):
    """Класс для вывода списка марок с указанием количества заказанных авто каждой марки"""

    queryset = CarBrand.objects.annotate(quantity=Sum('models__orders__quantity')).order_by('id')
    serializer_class = CarBrandWithCountSerializer
