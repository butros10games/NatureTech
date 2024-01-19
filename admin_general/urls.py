from django.urls import path
from .views import admin_index, booking_context, sort_bookings, create_modal, save_modal, usage_data, ip_logger, ip_adress_display, btn_logger, btn_state_display, pir_logger, pir_state_display, ble_logger, ble_state_display

urlpatterns = [
    path('', admin_index, name='booking_index'),
    path('booking_context/', booking_context, name='booking_context'),
    path('sort_bookings/', sort_bookings, name='sort_bookings'),
    path('create_modal/', create_modal, name='create_modal'),
    path('usage_data/', usage_data, name='usage_data'),
    path('save_modal/', save_modal, name='save_modal'),
    
    path('api/bt/<str:ip_adress>', ip_logger, name='ip_logger'),
    path('bt/ip_adress_display/', ip_adress_display, name='ip_adress_display'),

    path('api/btn/<str:ip_adress>/<str:state>', btn_logger, name='button_log'),
    path('btn/btn_state_display/', btn_state_display, name='btn_state_display'),

    path('api/pir/<str:ip_adress>/<str:PIR_state>', pir_logger, name='pir_log'),
    path('pir/pir_state_display/', pir_state_display, name='pir_state_display'),

    path('api/ble/<str:ip_adress>/<str:hostname>/<str:BLE_rssi>/<str:BLE_adress>/<str:BLE_name>/<str:BLE_count>', ble_logger, name='ble_log'),
    path('ble/ble_state_display/', ble_state_display, name='ble_state_display')
] 