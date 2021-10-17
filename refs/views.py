from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *

class ReflistHome(DataMixin, ListView):

    model=Reflist
    template_name = 'refs/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title='Гдавная страница')
        return dict(list(context.items())+list(c_def.items()))

class SearchList(DataMixin,ListView):
    form_class=SearchForm
    template_name = 'refs/search_results.html'
    model = Reflist
    context_object_name = 'posts'

    def get_queryset(self):
        query=self.request.GET.get('q')
        object_list=Reflist.objects.filter(title__icontains=query)
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title='Поиск')
        return dict(list(context.items())+list(c_def.items()))

def about(request):
    return render(request,'refs/about.html',{'menu':menu,'title':'О сайте'})

class AddWork(LoginRequiredMixin,DataMixin, CreateView):
    form_class = AddWorkForm
    template_name = 'refs/addwork.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *,object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title='Добавление работы')
        return dict(list(context.items())+list(c_def.items()))


class ContactFormView(DataMixin,FormView):
    form_class = ContactForm
    template_name = 'refs/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self,*,object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title='Обратная связь')
        return dict(list(context.items())+list(c_def.items()))

    def post(self,request):
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')

def pageNotFound(request, exception):
    return HttpResponseNotFound('Страница не найдена')

def down_work(request,work_id):
    return HttpResponse(f'Скачивание работы с id={work_id}')

class ReflistCategory(DataMixin,ListView):
    model=Reflist
    template_name = 'refs/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Reflist.objects.filter(cat__id=self.kwargs['cat_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title='Категория - '+str(context['posts'][0].cat),
                                    cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items())+list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'refs/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title='Регистрация')
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        user=form.save()
        login(self.request,user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class=LoginUserForm
    template_name='refs/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title='Авторизация')
        return dict(list(context.items())+list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('home')