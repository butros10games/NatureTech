from django.urls import path
from .views import index, contact, ip_logger, ip_adress_display

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    
    path('api/bt/<str:ip_adress>', ip_logger, name='ip_logger'),
    path('bt/ip_adress_display/', ip_adress_display, name='ip_adress_display')
]