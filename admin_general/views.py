from django.shortcuts import render, redirect
from booking_system.models import Booking, Customer
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string



# Create your views here.
def admin_index(request):
    ## if the user is not logged in, redirect to the login page
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'boer-admin/admin_general/admin_index.html')

def booking_context(request):
    if not request.user.is_authenticated:
        return redirect('login')

    bookings = Booking.objects.all().order_by('id')
    paginator = Paginator(bookings, 10)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Render the table rows as HTML
    return render(request, 'boer-admin/admin_general/admin_orders.html', {'page_obj': page_obj})


