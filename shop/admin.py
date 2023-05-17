from django.contrib import admin

from shop.models import CarBrand, CarModel, Color, Order


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ('id',)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand',)
    readonly_fields = ('id',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ('id',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('color', 'model', 'quantity', 'dt',)
    readonly_fields = ('id',)
    list_filter = ('model__brand', 'color',)
