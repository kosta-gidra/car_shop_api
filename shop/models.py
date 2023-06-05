from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class CarBrand(models.Model):
    name = models.CharField(max_length=100, verbose_name='Марка', unique=True)

    class Meta:
        verbose_name = 'Марка автомобиля'
        verbose_name_plural = "Марки автомобилей"

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(CarBrand, verbose_name='Марка', related_name='models', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Модель', unique=True)

    class Meta:
        verbose_name = 'Модель автомобиля'
        verbose_name_plural = "Модели автомобилей"

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name='Цвет')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = "Список цветов"

    def __str__(self):
        return self.name


class Order(models.Model):
    color = models.ForeignKey(Color, verbose_name='Цвет', related_name='orders', on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, verbose_name='Модель', related_name='orders', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество', validators=[MinValueValidator(1)])
    dt = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Список заказов"

    def __str__(self):
        return str(self.dt)

    @classmethod
    def show_brands(cls):
        """Метод для вывода словаря, содержащего мароки, с указанием количества заказанных авто каждой марки"""

        orders = cls.objects.all()
        result = {}
        for order in orders:
            if order.model.brand.name not in result:
                result[order.model.brand.name] = order.quantity
            else:
                result[order.model.brand.name] = result[order.model.brand.name] + order.quantity
        return result

    @classmethod
    def show_colors(cls):
        """Метод для вывода словаря, содержащего цвета, с указанием количества заказанных авто каждого цвета"""

        orders = cls.objects.all()
        result = {}
        for order in orders:
            if order.color.name not in result:
                result[order.color.name] = order.quantity
            else:
                result[order.color.name] = result[order.color.name] + order.quantity
        return result
