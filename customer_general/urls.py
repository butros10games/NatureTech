from django.urls import path
from .views import index, contact, ip_logger, ip_adress_display, faciliteiten, nieuws, btn_logger, btn_state_display, pir_logger, pir_state_display

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('faciliteiten/', faciliteiten, name='faciliteiten'),
    path('nieuws/', nieuws, name='nieuws'),
    
    path('api/bt/<str:ip_adress>', ip_logger, name='ip_logger'),
    path('bt/ip_adress_display/', ip_adress_display, name='ip_adress_display'),

    path('api/btn/<str:ip_adress>/<str:state>', btn_logger, name='button_log'),
    path('btn/btn_state_display/', btn_state_display, name='btn_state_display'),

    path('api/pir/<str:ip_adress>/<str:PIR_state>', pir_logger, name='pir_log'),
    path('pir/pir_state_display/', pir_state_display, name='pir_state_display')
]