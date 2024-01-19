from django.shortcuts import render, redirect
from booking_system.models import Booking, Customer, CampingSpot, PlekType
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import F
from .models import BtIpAdress, BtnState, pirState, BtMACAdress
import json
from django.db import transaction
from booking_system.views import calc_full_price

from django.http import HttpResponse, JsonResponse
import http


def admin_index(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')
    
    return render(request, 'boer-admin/admin_general/admin_index.html')


def booking_context(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')
    
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        bookings = Booking.objects.prefetch_related('customer', 'customer__user', 'CampingSpot').order_by('start_date').all()
        paginator = Paginator(bookings, 10)
        page_number = data.get('page', 1)
        page_obj_dict = []
        
        for booking in paginator.page(page_number).object_list:
            booking_dict = {
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
                'city': booking.customer.city,
                'street': booking.customer.street,
                'house_number': booking.customer.house_number,
                'postal_code': booking.customer.postal_code,
            }

            if booking.CampingSpot is not None:
                booking_dict['Campingspot'] = booking.CampingSpot.plekNummer if booking.CampingSpot.plekNummer is not None else None
            else:
                booking_dict['Campingspot'] = None

            if booking.CampingSpot is not None:
                booking_dict['Campingspot'] = booking.CampingSpot.plekNummer if booking.CampingSpot.plekNummer is not None else None
                total_days_price = calc_full_price(booking.start_date, booking.end_date, booking.CampingSpot.plekType)
            else:
                booking_dict['Campingspot'] = None
                total_days_price = 0

            booking_dict['total_price'] = total_days_price

            

            page_obj_dict.append(booking_dict)

        return JsonResponse(page_obj_dict, safe=False)

    return render(request, 'boer-admin/admin_general/admin_orders.html')


def sort_bookings(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        page_number = data.get('page' , 1)
        sort_by = data.get('sort_by', 'start_date') 
        order = data.get('order', 'asc')

        # Retrieve and sort the bookings
        bookings = Booking.objects.prefetch_related('customer', 'customer__user', 'CampingSpot').order_by('start_date').all()

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
            booking_dict = {
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
                'city': booking.customer.city,
                'street': booking.customer.street,
                'house_number': booking.customer.house_number,
                'postal_code': booking.customer.postal_code,
            }

            if booking.CampingSpot is not None:
                booking_dict['Campingspot'] = booking.CampingSpot.plekNummer if booking.CampingSpot is not None else None
            else:
                booking_dict['Campingspot'] = None
            if booking.CampingSpot is not None:
                total_days_price = calc_full_price(booking.start_date, booking.end_date, booking.CampingSpot.plekType)
            else:
                total_days_price = 0 

            booking_dict['total_price'] = total_days_price

            page_obj_dict.append(booking_dict)

        return JsonResponse(page_obj_dict, safe=False)

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

            total_price = calc_full_price(booking.start_date, booking.end_date, booking.CampingSpot.plekType)

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
                'city': booking.customer.city,
                'street': booking.customer.street,
                'house_number': booking.customer.house_number,
                'postal_code': booking.customer.postal_code,
                'Campingspot': booking.CampingSpot.PlekNummer, 
            }
            if booking.CampingSpot is not None:
                booking_data['Campingspot'] = booking.CampingSpot.PlekNummer
            else:
                booking_data['Campingspot'] = None
            if booking.CampingSpot is not None:
                total_days_price = calc_full_price(booking.start_date, booking.end_date, booking.CampingSpot.plekType)
            else:
                total_days_price = 0 
            booking_data['total_price'] = total_days_price




            return JsonResponse(booking_data, safe=False)
        else:
            return JsonResponse({'error': 'Missing booking_id in modal_data'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def save_modal(request):
    if request.method == 'POST':
        try:
            modal_data = json.loads(request.body.decode('utf-8')).get('modal_data')
            if modal_data is None:
                raise ValueError('Missing or invalid modal_data')
        except (json.JSONDecodeError, ValueError) as e:
            return JsonResponse({'error': f'Missing or invalid modal_data: {e}'}, status=400)

        booking_id = modal_data.get('id')
        if booking_id is not None:
            try:
                booking = Booking.objects.prefetch_related('customer', 'customer__user', 'CampingSpot', ).get(id=booking_id)
            except Booking.DoesNotExist:
                return JsonResponse({'error': 'Booking not found'}, status=404)

            # Update the booking data
            booking.customer.first_name = modal_data.get('first_name')
            booking.customer.last_name = modal_data.get('last_name')
            booking.customer.user.email = modal_data.get('email')
            booking.customer.phone_number = modal_data.get('phone_number')
            booking.customer.street = modal_data.get('street')
            booking.customer.house_number = modal_data.get('house_number')
            booking.customer.postal_code = modal_data.get('postal_code')
            booking.customer.city = modal_data.get('city')
            booking.start_date = modal_data.get('start_date')
            booking.end_date = modal_data.get('end_date')
            booking.age_above = modal_data.get('age_above')
            booking.age_below = modal_data.get('age_below')
            # booking.CampingSpot.plekNummer = modal_data.get('Campingspot')
            booking.checked_in = modal_data.get('checked_in')
            booking.paid = modal_data.get('paid')
            booking.notes = modal_data.get('notes')
            booking.admin_notes = modal_data.get('admin_notes')
            
            #Save the update booking data to the database (Booking, Customer, User)
            with transaction.atomic():
                booking.customer.user.save()
                booking.customer.save()
                booking.save()
        

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Missing booking_id in modal_data'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)



def usage_data(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')
    
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


########### PI code ###########
def ip_logger(request, ip_adress):
    BtIpAdress.objects.create(ip_adress=ip_adress)
    
    return HttpResponse(status=http.HTTPStatus.OK) # 200 OK

def ip_adress_display(request):
    ## Make it so that only the last 10 ip adresses are displayed and the newest one is on top
    ip_adresses = BtIpAdress.objects.all().order_by('-date')[:10]

    context = {
        "ip_adresses": ip_adresses
    }

    return render(request, 'boer-admin/ble/ip_adress_display.html', context=context)

def btn_logger(request, ip_adress, state):
    ## string to bool converter
    if state == "1":
        state = True
    elif state == "0":
        state = False
    else:
        return HttpResponse(status=http.HTTPStatus.BAD_REQUEST) # 400 Bad Request
    
    BtnState.objects.create(state=state, ip_adress=ip_adress)
    
    return HttpResponse(status=http.HTTPStatus.OK) # 200 OK

def btn_state_display(request):
    ## Make it so that only the last 10 ip adresses are displayed and the newest one is on top
    btn_states = BtnState.objects.all().order_by('-date')[:10]

    context = {
        "btn_states": btn_states
    }

    return render(request, 'boer-admin/ble/btn_state_display.html', context=context)

def pir_logger(request, ip_adress, PIR_state, ):
    ## string to bool converter
    if PIR_state == "1":
        PIR_state = True
    elif PIR_state == "0":
        PIR_state = False
    else:
        return HttpResponse(status=http.HTTPStatus.BAD_REQUEST) # 400 Bad Request
    
    pirState.objects.create(PIR_state=PIR_state, ip_adress=ip_adress)
    
    return JsonResponse({'status': 'Ok'})

def pir_state_display(request):
    ## Make it so that only the last 10 ip adresses are displayed and the newest one is on top
    pir_states = pirState.objects.all().order_by('-date')[:10]

    context = {
        "pir_states": pir_states
    }

    return render(request, 'boer-admin/ble/pir_state_display.html', context=context)

def ble_logger(request, ip_adress, hostname, BLE_rssi, BLE_adress, BLE_name, BLE_count):
    BtMACAdress.objects.create(ip_adress=ip_adress, hostname=hostname,BLE_rssi=BLE_rssi, BLE_adress=BLE_adress, BLE_name=BLE_name, BLE_count=BLE_count)
    
    return JsonResponse({'status': 'Ok'})

def ble_state_display(request):
    ## Make it so that only the last 10 ip adresses are displayed and the newest one is on top
    BLE_adresses = BtMACAdress.objects.all().order_by('-date')[:100]

    context = {
        "BLE_adresses": BLE_adresses
    }

    return render(request, 'boer-admin/ble/ble_state_display.html', context=context)