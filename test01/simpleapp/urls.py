from django.urls import path
# Импортируем созданное нами представление
from .views import ProductsList, ProductDetail, ProductCreate, ProductUpdate, ProductDelete, create_product, AppointmentView


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', ProductsList.as_view(), name='product_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   #path('<int:pk>', ProductDetail.as_view()),
   path('<int:pk>/', ProductDetail.as_view(), name= 'product_detail'),
   path('createdef/', create_product, name= 'product_createdef'),
   path('create/', ProductCreate.as_view(), name='product_create'),
   path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
   path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
   path('appointments/', AppointmentView.as_view(), name='appointments'),

]


