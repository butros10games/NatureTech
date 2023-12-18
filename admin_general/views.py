from django.shortcuts import render, redirect
from booking_system.models import Booking, Customer, CampingSpot, PlekType
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

        valid_sort_fields = ['order_number', 'start_date', 'end_date', 'age_below', 'age_above', 'pdf', 'checked_in', 'paid']

        if sort_by in valid_sort_fields:
            if order == 'asc':
                bookings = bookings.order_by(F(sort_by).asc(nulls_last=True))
            elif order == 'desc':
                bookings = bookings.order_by(F(sort_by).desc(nulls_last=True))
        elif sort_by == 'firstname':
            if order == 'asc':
                bookings = bookings.order_by(F('customer__user__last_name').asc(nulls_last=True))
            elif order == 'desc':
                bookings = bookings.order_by(F('customer__user__last_name').desc(nulls_last=True))
        elif sort_by == 'email':
            if order == 'asc':
                bookings = bookings.order_by(F('customer__user__email').asc(nulls_last=True))
            elif order == 'desc':
                bookings = bookings.order_by(F('customer__user__email').desc(nulls_last=True))
        elif sort_by == 'phone_number':
            if order == 'asc':
                bookings = bookings.order_by(F('customer__phone_number').asc(nulls_last=True))
            elif order == 'desc':
                bookings = bookings.order_by(F('customer__phone_number').desc(nulls_last=True))



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
 