from django.db import IntegrityError
from rest_framework import serializers

from shop.models import CarBrand, CarModel, Color, Order


class CarBrandSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(min_length=3)


class CarModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModel
        fields = ('id', 'name', 'brand')


class FullCarBrandSerializer(CarBrandSerializer):
    models = CarModelSerializer(read_only=True, many=True)

    def create(self, validated_data):
        try:
            brand = CarBrand.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'Error': 'Марка не создана'})
        else:
            return brand

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class FullCarModelSerializer(CarModelSerializer):
    brand = CarBrandSerializer(read_only=True)


class ColorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=3)

    class Meta:
        model = Color
        fields = ('id', 'name')


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'dt', 'color', 'model', 'quantity')


class FullOrderSerializer(OrderSerializer):
    model = FullCarModelSerializer(read_only=True)
    color = ColorSerializer(read_only=True)


class ColorWithCountSerializer(ColorSerializer):
    total_quantity = serializers.IntegerField(source='quantity', read_only=True)
    # color_id = serializers.IntegerField(source='id')
    color = serializers.CharField(source='name')

    class Meta(ColorSerializer.Meta):
        fields = ('color', 'total_quantity')


class CarBrandWithCountSerializer(CarBrandSerializer):
    total_quantity = serializers.IntegerField(source='quantity', read_only=True)
