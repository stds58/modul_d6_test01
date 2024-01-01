import django_filters
from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter
from .models import Product, Material

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.


class ProductFilter(FilterSet):
    # material = django_filters.ModelChoiceFilter(
    #     field_name='productmaterial__material',
    #     queryset=Material.objects.all(),
    #     label='Material',
    #     empty_label = 'любой'
    # )
    material = ModelMultipleChoiceFilter(
        field_name = 'productmaterial__material',
        queryset = Material.objects.all(),
        label = 'Material',
        conjoined=True
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Product
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            # 'productmaterial__material': ['exact'],
            'name': ['icontains'],
            # количество товаров должно быть больше или равно
            'quantity': ['gt'],
            'price': [
                'lt',  # цена должна быть меньше или равна указанной
                'gt',  # цена должна быть больше или равна указанной
            ],
        }

