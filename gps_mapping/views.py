from django.shortcuts import render, redirect
from django.http import JsonResponse
import traceback

from django.middleware.csrf import get_token

from booking_system.models import Veld, VeldGps

# Create your views here.
def gps_index(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')
    
    return render(request, 'boer-admin/gps_mapping/gps_index.html')

def gps_scan(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')
    
    context = {
        'csrf_token': get_token(request),
    }
    return render(request, 'boer-admin/gps_mapping/gps_scan.html', context)

# Gets a post request with all the gps data points and saves them to the database
def gps_scan_save(request):
    # Respond only to POST requests
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "This is not a POST request."})

    try:
        pass
    
        return JsonResponse({"status": "success"})

    except Exception as e:
        # Log the error if needed
        return JsonResponse({"status": "error", "message": str(e), "traceback": traceback.format_exc()})
    
def veld_gps_saving(request):
    if request.method == 'POST':
        try:
            veld = request.POST['veld']
            gps_locations = request.POST['gps_locations']
            
            veld_object = Veld.objects.create(id=veld)

            for gps_location in gps_locations:
                VeldGps.objects.create(veld=veld_object, lat=gps_location['lat'], lng=gps_location['lng'])
            
            return JsonResponse({"status": "success"})
        
        except Exception as e:
            # Log the error if needed
            return JsonResponse({"status": "error", "message": str(e), "traceback": traceback.format_exc()})