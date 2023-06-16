import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from shop.models import CarBrand, CarModel, Color, Order


@pytest.fixture()
def client():
    """Фикстура создания клиента"""

    return APIClient()


@pytest.fixture()
def create_brand():
    """Фикстура создания марки"""

    brand = CarBrand.objects.create(name='Subaru')
    return brand


@pytest.fixture()
def create_model(create_brand):
    """Фикстура создания модели"""

    model = CarModel.objects.create(name='Legacy', brand_id=create_brand.id)
    return model


@pytest.fixture()
def create_orders():
    """Фикстура создания заказов"""

    color1 = Color.objects.create(name='red')  # total 10
    color2 = Color.objects.create(name='blue')  # total 7
    brand1 = CarBrand.objects.create(name='Subaru')  # total 14
    brand2 = CarBrand.objects.create(name='Honda')  # total 3
    model1 = CarModel.objects.create(name='Legacy', brand_id=brand1.id)
    model2 = CarModel.objects.create(name='Forester', brand_id=brand1.id)
    model3 = CarModel.objects.create(name='Accord', brand_id=brand2.id)
    orders = Order.objects.bulk_create([Order(color_id=color1.id, model_id=model1.id, quantity='5'),
                                        Order(color_id=color1.id, model_id=model2.id, quantity='5'),
                                        Order(color_id=color2.id, model_id=model2.id, quantity='4'),
                                        Order(color_id=color2.id, model_id=model3.id, quantity='3')])
    return orders


@pytest.mark.django_db
def test_brand(client):
    """Тест создания марки автомобиля"""

    response = client.post('/api/brand/', data=dict(name='Subaru'))

    brand = CarBrand.objects.get(name='Subaru')

    assert brand
    assert response.status_code == 201


@pytest.mark.django_db
def test_model(client, create_brand):
    """Тест создания модели автомобиля"""

    response = client.post('/api/model/', data=dict(name='Legacy', brand=create_brand.id))

    model = CarModel.objects.get(name='Legacy', brand_id=create_brand.id)

    assert model
    assert response.status_code == 201


@pytest.mark.django_db
def test_order(client, create_model):
    """Тест создания заказа"""

    color = Color.objects.create(name='gray')
    date_string = f'{timezone.now():%Y-%m-%d %H:%M:%S%z}'

    response = client.post('/api/order/', data=dict(dt=date_string,
                                                    color=color.id,
                                                    model=create_model.id,
                                                    quantity='1'))

    data = response.json()
    order = Order.objects.get(id=data['id'], dt=date_string, color=color.id, model=create_model.id, quantity='1')

    assert order
    assert response.status_code == 201


@pytest.mark.django_db
def test_color_inform(client, create_orders):
    """Тест вывода списка цветов с указанием количества заказанных авто каждого цвета"""

    response = client.get('/api/color_inform/')
    response_data = response.json()

    data = {}
    for color in response_data:
        data[color['color']] = color['total_quantity']

    assert data['red'] == 10
    assert data['blue'] == 7
    assert response.status_code == 200


@pytest.mark.django_db
def test_brand_inform(client, create_orders):
    """Тест вывода списка марок с указанием количества заказанных авто каждой марки"""

    response = client.get(f'/api/brand_inform/')
    response_data = response.json()

    data = {}
    for brand in response_data:
        data[brand['name']] = brand['total_quantity']

    assert data['Subaru'] == 14
    assert data['Honda'] == 3
    assert response.status_code == 200
