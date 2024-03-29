from django.shortcuts import render, reverse, redirect
from datetime import datetime
from pprint import pprint
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.views.generic.edit import CreateView
from .models import Product #, Appointment
from .filters import ProductFilter
from .forms import ProductForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from django.core.mail import mail_admins # импортируем функцию для массовой отправки писем админам


@method_decorator(login_required, name='dispatch')
#@method_decorator(login_required(login_url = '/about/'), name='dispatch')
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
    paginate_by = 2  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ProductFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.now()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = "Распродажа в среду!"
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        #pprint(context)
        return context


class ProductDetail(LoginRequiredMixin, DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Product
    # Используем другой шаблон — product.html
    template_name = 'product.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'product'
    #
    #pk_url_kwarg = 'pk'


# Добавляем новое представление для создания товаров.
class ProductCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_product',)
    # а дальше пишите код вашего представления
    # Указываем нашу разработанную форму
    form_class = ProductForm
    # модель товаров
    model = Product
    # и новый шаблон, в котором используется форма.
    template_name = 'product_edit.html'


# Добавляем представление для изменения товара.
class ProductUpdate(UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'


# Представление удаляющее товар.
class ProductDelete(DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')


def create_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/products')


    return render(request, 'product_edit.html', {'form':form})


# class AppointmentView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'make_appointment.html', {})
#
#     def post(self, request, *args, **kwargs):
#         appointment = Appointment(
#             date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
#             client_name=request.POST['client_name'],
#             message=request.POST['message'],
#         )
#         appointment.save()
#
#         # # отправляем письмо
#         # send_mail(
#         #     subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
#         #     # имя клиента и дата записи будут в теме для удобства
#         #     message=appointment.message,  # сообщение с кратким описанием проблемы
#         #     from_email='peterbadson@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
#         #     recipient_list=[]  # здесь список получателей. Например, секретарь, сам врач и т. д.
#         # )
#         # # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
#         # mail_admins(
#         #     subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
#         #     message=appointment.message,
#         # )
#
#         # получаем наш html
#         html_content = render_to_string(
#             'appointment_created.html',
#             {
#                 'appointment': appointment,
#             }
#         )
#
#         # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
#         msg = EmailMultiAlternatives(
#             subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
#             body=appointment.message,  # это то же, что и message
#             from_email='stds58@yandex.ru',
#             to=['stds58@gmail.com'],  # это то же, что и recipients_list
#         )
#         msg.attach_alternative(html_content, "text/html")  # добавляем html
#         msg.send()  # отсылаем
#
#         return redirect('appointments:make_appointment')


#https://github.com/Tpe3B/NewsPaper/blob/master/NewsPaper/NewsPaper/urls.py
#2022-03-31

