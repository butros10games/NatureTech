from django.shortcuts import render
from booking_system.models import Booking, Customer
from django.contrib.auth.models import User


# Create your views here.
def admin_index(request):
    return booking_context(request)

def booking_context(request):
    bookings = Booking.objects.all().order_by('id')

    # Pass the bookings data to the template
    context = {
        'bookings': bookings,
    }

    return render(request, 'boer-admin/admin_general/admin_index.html', context)

