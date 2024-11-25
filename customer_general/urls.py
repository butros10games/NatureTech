from django.urls import path

from .views import contact, faciliteiten, index, nieuws

urlpatterns = [
    path("", index, name="index"),
    path("contact/", contact, name="contact"),
    path("faciliteiten/", faciliteiten, name="faciliteiten"),
    path("nieuws/", nieuws, name="nieuws"),
]
