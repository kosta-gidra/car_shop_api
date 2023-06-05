from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from shop.models import CarBrand, CarModel, Color, Order
from shop.serializers import ColorSerializer, OrderSerializer, FullCarBrandSerializer, \
    FullOrderSerializer, CarModelSerializer


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

    # заменил сериалайзер в методах list и retrieve, чтобы получать расширенную информацию по заказам

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FullOrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FullOrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = FullOrderSerializer(instance)
        return Response(serializer.data)


class ColorInformView(APIView):
    """Класс для вывода списка цветов с указанием количества заказанных авто каждого цвета"""

    def get(self, request, *args, **kwargs):
        result = Order.show_colors()
        return JsonResponse(result)


class BrandInformView(APIView):
    """Класс для вывода списка марок с указанием количества заказанных авто каждой марки"""

    def get(self, request, *args, **kwargs):
        result = Order.show_brands()
        return JsonResponse(result)
