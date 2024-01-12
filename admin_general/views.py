from django.shortcuts import render, redirect
from booking_system.models import Booking, Customer, CampingSpot, PlekType
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import F
from customer_general.models import BtIpAdress, BtnState, pirState, BtMACAdress
import json


def admin_index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'boer-admin/admin_general/admin_index.html')

def booking_context(request):
    # respond to the JS fetch request
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        bookings = Booking.objects.prefetch_related('customer', 'customer__user').order_by('start_date').all()
        paginator = Paginator(bookings, 10)
        page_number = data.get('page', 1)

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
                'id': booking.id,
            })

        data = page_obj_dict
        return JsonResponse(data, safe=False)

    return render(request, 'boer-admin/admin_general/admin_orders.html')

def sort_bookings(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        page_number = data.get('page', 1)
        sort_by = data.get('sort_by') 
        order = data.get('order', 'asc')

        # Retrieve and sort the bookings
        bookings = Booking.objects.prefetch_related('customer', 'customer__user').all()

        valid_sort_fields = ['order_number', 'start_date', 'end_date', 'age_below', 'age_above', 'pdf', 'checked_in', 'paid']

        if sort_by in valid_sort_fields:
            if order == 'asc':
                bookings = bookings.order_by(F(sort_by).asc(nulls_last=True))
            elif order == 'desc':
                bookings = bookings.order_by(F(sort_by).desc(nulls_last=True))
        elif sort_by == 'lastname':
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
                'id': booking.id,	
                

            })

        data = page_obj_dict
        return JsonResponse(data, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)
 
def create_modal(request):
    if request.method == 'POST':
        try:
            modal_data = json.loads(request.POST.get('modal_data'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data in modal_data'}, status=400)

        # Fetch the booking, customer, and user data using the id's from the modal_data
        booking_id = modal_data.get('booking_id')
        if booking_id is not None:
            try:
                booking = Booking.objects.prefetch_related('customer', 'customer__user').get(id=booking_id)
            except Booking.DoesNotExist:
                return JsonResponse({'error': 'Booking not found'}, status=404)

            # Create a dictionary with the data from the booking, customer, and user
            booking_data = {
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
                'id': booking.id,
            }

            return JsonResponse(booking_data, safe=False)
        else:
            return JsonResponse({'error': 'Missing booking_id in modal_data'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def usage_data(request):
    bt_ip_data = BtIpAdress.objects.values('ip_adress')
    btn_state_data = BtnState.objects.values('ip_adress', 'state')
    pir_state_data = pirState.objects.values('ip_adress', 'PIR_state')
    bt_mac_data = BtMACAdress.objects.values('ip_adress', 'hostname', 'BLE_count')

    combined_data = {}

    for data in bt_ip_data:
        ip_adress = data['ip_adress']
        if ip_adress not in combined_data:
            combined_data[ip_adress] = {'ip_adress': ip_adress}

    for data in btn_state_data:
        ip_adress = data['ip_adress']
        if ip_adress in combined_data:
            combined_data[ip_adress].update(data)

    for data in pir_state_data:
        ip_adress = data['ip_adress']
        if ip_adress in combined_data:
            combined_data[ip_adress].update(data)

    for data in bt_mac_data:
        ip_adress = data['ip_adress']
        if ip_adress in combined_data:
            combined_data[ip_adress].update(data)

    sorted_data = sorted(combined_data.values(), key=lambda x: x['ip_adress'])

    return render(request, 'boer-admin/admin_general/usage_data.html', {'data': sorted_data})
    # return JsonResponse(list(combined_data.values()), safe=False)