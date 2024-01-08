from django.shortcuts import render
from django.http import JsonResponse
import traceback

# Create your views here.
def gps_index(request):
    return render(request, 'boer-admin/gps_mapping/gps_index.html')

def gps_scan(request):
    return render(request, 'boer-admin/gps_mapping/gps_scan.html')

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