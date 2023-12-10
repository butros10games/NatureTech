from django.shortcuts import render, redirect
from booking_system.models import Booking, Customer
from django.contrib.auth.models import User


# Create your views here.
def admin_index(request):
    ## if the user is not logged in, redirect to the login page
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'boer-admin/admin_general/admin_index.html')

def booking_context(request):
    ## if the user is not logged in, redirect to the login page
    if not request.user.is_authenticated:
        return redirect('login')
    
    bookings = Booking.objects.all().order_by('id')

    # Pass the bookings data to the template
    context = {
        'bookings': bookings,
    }

    return render(request, 'boer-admin/admin_general/admin_orders.html', context)
