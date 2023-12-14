from django.shortcuts import render, redirect
from booking_system.models import Booking, Customer 
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import F


def admin_index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'boer-admin/admin_general/admin_index.html')

def booking_context(request):
    if request.method == 'POST':
        page_number = request.POST.get('page', 1)
        bookings = Booking.objects.prefetch_related('customer', 'customer__user').all()
        paginator = Paginator(bookings, 10)

        page_obj_dict = []
        for booking in paginator.page(page_number).object_list:
            page_obj_dict.append({
                'firstname': booking.customer.user.first_name,
                'lastname': booking.customer.user.last_name,
                'email': booking.customer.user.email,
                'phone_number': booking.customer.phone_number,
                'order_number': booking.order_number,
                'start_date': booking.start_date,
                'end_date': booking.end_date,
                'age_below': booking.age_below,
                'age_above': booking.age_above,
                'pdf': booking.pdf,
                'checked_in': booking.checked_in,
                'paid': booking.paid,
            })

        data = page_obj_dict
        return JsonResponse(data, safe=False)

    return render(request, 'boer-admin/admin_general/admin_orders.html')

def sort_bookings(request):
    if request.method == 'POST':
        page_number = request.POST.get('page', 1)
        sort_by = request.POST.get('sort_by') 
        order = request.POST.get('order', 'asc') 
        # Retrieve and sort the bookings
        bookings = Booking.objects.prefetch_related('customer', 'customer__user').all()
        if order == 'asc':
            bookings = bookings.order_by(sort_by)
        else:
            bookings = bookings.order_by(F(sort_by).desc())

        # Apply pagination
        paginator = Paginator(bookings, 10)
        page_obj_dict = []
        for booking in paginator.page(page_number).object_list:
            page_obj_dict.append({
                'firstname': booking.customer.user.first_name,
                'lastname': booking.customer.user.last_name,
                'email': booking.customer.user.email,
                'phone_number': booking.customer.phone_number,
                'order_number': booking.order_number,
                'start_date': booking.start_date,
                'end_date': booking.end_date,
                'age_below': booking.age_below,
                'age_above': booking.age_above,
                'pdf': booking.pdf,
                'checked_in': booking.checked_in,
                'paid': booking.paid,
            })

        data = page_obj_dict
        return JsonResponse(data, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)
 