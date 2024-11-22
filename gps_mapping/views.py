from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import JsonResponse
import traceback
import json

from django.middleware.csrf import get_token

from booking_system.models import Veld, VeldGps, Veldvulling


# Create your views here.
def gps_index(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect("login")

    fields = Veld.objects.all()
    fields_json = []

    for field in fields:
        veldvullingen = Veldvulling.objects.filter(Veld=field)
        places = []
        total_places = 0
        for veldvulling in veldvullingen:
            places.append(
                {"name": veldvulling.PlekType.name, "number": veldvulling.number}
            )
            total_places += veldvulling.number

        fields_json.append(
            {
                "id": field.id,
                "name": field.name,
                "total_places": total_places,
                "places": places,
            }
        )

    context = {
        "csrf_token": get_token(request),
        "fields": fields_json,
    }

    return render(request, "boer-admin/gps_mapping/gps_index.html", context)


def gps_scan(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect("login")

    context = {
        "csrf_token": get_token(request),
    }
    return render(request, "boer-admin/gps_mapping/gps_scan.html", context)


# Gets a post request with all the gps data points and saves them to the database
def gps_scan_save(request):
    # Respond only to POST requests
    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "This is not a POST request."}
        )

    try:
        pass

        return JsonResponse({"status": "success"})

    except Exception as e:
        # Log the error if needed
        return JsonResponse(
            {"status": "error", "message": str(e), "traceback": traceback.format_exc()}
        )


def veld_gps_saving(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            gps_locations = data.get("path")

            # get the name of the last field
            last_field = Veld.objects.last()

            # it is a, b, c naming system so how to get the next letter?
            # get the last letter
            last_letter = last_field.name
            # get the next letter
            next_letter = chr(ord(last_letter) + 1)
            veld_object = Veld.objects.create(name=next_letter)

            for gps_location in gps_locations:
                VeldGps.objects.create(
                    veld=veld_object, lat=gps_location["lat"], lng=gps_location["lng"]
                )

            return JsonResponse({"status": "success"})

        except Exception as e:
            # Log the error if needed
            return JsonResponse(
                {
                    "status": "error",
                    "message": str(e),
                    "traceback": traceback.format_exc(),
                }
            )


def field_display(request, field_id):
    field = Veld.objects.get(id=field_id)
    gps_locations = VeldGps.objects.filter(veld=field)
    gps_data = []

    for gps in gps_locations:
        gps_data.append({"lat": gps.lat, "lng": gps.lng})

    context = {
        "field": field,
        "gps_data": gps_data,
    }

    return render(request, "boer-admin/gps_mapping/gps_display.html", context)
