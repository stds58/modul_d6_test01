from django.shortcuts import render

# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView
from .models import Product


class ProductsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Product
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'name'

    #если надо показать записи где цена меньше 300, то вместо верхнего примера пишем:
    #qyeryset = Product.objects.filter(price__lt=300).order_by('-name')

    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'products.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    # как здесь указали products так и в файле products.html его указываем:{% block content %}  <h1>Все товары</h1>  {{ products }}  {% endblock content %}
    # если названия будут отличаться,в products.html ничего не отобразится
    context_object_name = 'products'


class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Product
    # Используем другой шаблон — product.html
    template_name = 'product.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'product'
    #
    pk_url_kwarg = 'quantity'