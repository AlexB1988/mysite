from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns=[
    path('',ReflistHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('addwork/',AddWork.as_view(), name='add_work'),
    path('contact/', ContactFormView.as_view(),name='contact'),
    path('login/',LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/',RegisterUser.as_view(), name='register'),
    path('work/<int:work_id>',down_work, name='work'),
    path('category/<int:cat_id>',ReflistCategory.as_view(), name='category'),
    path('search', SearchList.as_view(), name='search'),

]