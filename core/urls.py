from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('menu/', views.menu, name='menu'),
    path('contact/', views.contact, name='contact'),
    path('booking/', views.booking, name='booking'),
    path('team/', views.team, name='team'),           
    path('testimonial/', views.testimonial, name='testimonial'),
    path('booking/', views.booking_view, name='booking'),
    path('i18n/', include('django.conf.urls.i18n')),
]