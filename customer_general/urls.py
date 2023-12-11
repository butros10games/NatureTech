from django.urls import path
from .views import index, contact, ip_logger, ip_adress_display, faciliteiten, nieuws, btn_logger, btn_state_display

urlpatterns = [
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('faciliteiten/', faciliteiten, name='faciliteiten'),
    path('nieuws/', nieuws, name='nieuws'),
    
    path('api/bt/<str:ip_adress>', ip_logger, name='ip_logger'),
    path('bt/ip_adress_display/', ip_adress_display, name='ip_adress_display'),

    path('api/btn/<str:ip_adress>/<bool:state>', btn_logger, name='button_log'),
    path('btn/btn_state_display/', btn_state_display, name='btn_state_display')


]