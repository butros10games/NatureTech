from django.shortcuts import render, redirect
from booking_system.models import Booking
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

from django.forms.models import model_to_dict



# Create your views here.
def admin_index(request):
    ## if the user is not logged in, redirect to the login page
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'boer-admin/admin_general/admin_index.html')

def booking_context(request):
    if request.method == 'POST':
        # Get the page number from the POST request
        page_number = request.POST.get('page', 1)
        
        # Get the bookings from the database
        bookings = Booking.objects.all().order_by('id')
        paginator = Paginator(bookings, 10)
        
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page_obj = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page_obj = paginator.page(paginator.num_pages)
            
        # Serialize the data
        data = [model_to_dict(obj) for obj in page_obj.object_list]
            
        # Return a json response
        return JsonResponse(data, safe=False)

    # Render the table rows as HTML
    return render(request, 'boer-admin/admin_general/admin_orders.html')
