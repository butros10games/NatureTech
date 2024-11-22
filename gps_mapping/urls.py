from django.urls import path
from .views import gps_index, gps_scan, veld_gps_saving, field_display

urlpatterns = [
    path("", gps_index, name="gps_index"),
    path("gps_scan/", gps_scan, name="gps_scan"),
    path("map/<uuid:field_id>", field_display, name="field_display"),
    path("api/veld_gps_saving/", veld_gps_saving, name="veld_gps_saving"),
]
