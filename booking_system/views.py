import re
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.conf import settings

from django_ratelimit.decorators import ratelimit

from .models import Booking, Customer, PlekType, Price, CampingSpot, Veldvulling, Veld
from django.contrib.auth.models import User

from django.db.models import Q

import traceback

import datetime

@ratelimit(key='ip', rate='3/60m')  # Limit to 5 requests per 15 minutes per IP address
def booking_form(request):
    if getattr(request, 'limited', False):
        return JsonResponse({"status": "error", "type": "rate_limit", "message": "You have exceeded the rate limit. Please wait before trying again."})
    
    if request.method == 'POST':
        try:
            first_name = request.POST['firstName']
            last_name = request.POST['lastName']
            phone_number = request.POST['phone']
            adults = request.POST['adults']
            childeren = request.POST['children']
            mail = request.POST['email']
            start = request.POST['startDate']
            end = request.POST['endDate']
            accomodation = request.POST['accomodation']

            user, created = User.objects.get_or_create(email=mail)
            if created:
                user.username = mail
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                
            veld = Veld.objects.all().first()
                
            # Check if all the campingspots are created
            all_plek_types = PlekType.objects.all()
            
            number_of_spots = {}
            
            for plek_type in all_plek_types:
                number_of_spots[plek_type.id] = Veldvulling.objects.get(PlekType=plek_type, Veld=veld).number
                
            ## Check the number of CampingSpots for each PlekType and create them if needed
            for plek_type in all_plek_types:
                number_of_spots = Veldvulling.objects.get(PlekType=plek_type, Veld=veld).number
                number_of_spots_created = CampingSpot.objects.filter(plekType=plek_type).count()
                
                if number_of_spots_created < number_of_spots:
                    for i in range(number_of_spots_created, number_of_spots):
                        CampingSpot.objects.create(plekNummer=i, plekType=plek_type, veld=veld)


            # Get all the bookingen that are in the same time period or with the end date or start date in the time period
            bookings = Booking.objects.filter(start_date__lte=end, end_date__gte=start)
            
            # Get all the places that are booked in the time period
            booked_places = []
            
            for booking in bookings:
                if booking.CampingSpot is not None:
                    booked_places.append(booking.CampingSpot.id)
                
            # Get the place that is requested
            plek_type_object = PlekType.objects.get(id=accomodation)
            
            # Get all the camping places
            camping_spot_all = CampingSpot.objects.filter(plekType=plek_type_object)
            
            # remove the booked places from the campingSpot_all
            for camping_spot in camping_spot_all:
                if camping_spot.id in booked_places:
                    camping_spot_all = camping_spot_all.exclude(id=camping_spot.id)
                    
            # Get the first place that is not booked
            accomodation_object = camping_spot_all.first()
            
            if accomodation_object is None:
                return JsonResponse({"status": "error", "type": "no_places", "message": "There are no places available for the selected time period."})
                

            customer, created = Customer.objects.get_or_create(user=user, phone_number=phone_number)
            booking_created = Booking.objects.create(customer=customer, age_above=adults, age_below=childeren, start_date=start, end_date=end, CampingSpot=accomodation_object)
            booking = booking_created if isinstance(booking_created, Booking) else None
            created = True  # Assuming the object is always created in this context

            ## reload booking out of the database
            booking.refresh_from_db()

            context = {
                "first_name": first_name,
                "last_name": last_name,
                "date_of_arrival": start,
                "date_of_departure": end,
                "accomodation": accomodation_object.plekType.name,
                "order_number": booking.order_number,
                "price": end,
                "method_of_paying": end,
                "adults": adults,
                "children": childeren
            }

            html_message = render_to_string("boer/booking/confirmation_mail.html", context=context)
            plain_message = strip_tags(html_message)

            message = EmailMultiAlternatives(
                subject = 'Bevestiging voor uw reservering op Camping de Groene Weide', 
                body = plain_message,
                from_email = None ,
                to= {mail}
            )

            message.attach_alternative(html_message, "text/html")
            message.send()

            # Second email to the specified email address
            html_message_admin = render_to_string("boer/booking/confirmation_mail_admin.html", context=context)
            plain_message_admin = strip_tags(html_message_admin)

            message_admin = EmailMultiAlternatives(
                subject='Nieuwe boeking ontvangen',
                body=plain_message_admin,
                from_email=mail,  # Use your default email address or specify one
                to=[settings.DEFAULT_FROM_EMAIL],  # Use a list for the 'to' parameter
            )
            message_admin.attach_alternative(html_message_admin, "text/html")
            message_admin.send()

            messages.success(request,f'Dankuwel, {first_name} {last_name}, voor het reserveren van een kampeerplek van {start} tot {end}. Een bevestigingsmail is verstuurd naar {mail}!')

            return JsonResponse({"status": "success"})
        
        except Exception as e:
            # Log the error if needed
            return JsonResponse({"status": "error", "message": str(e), "traceback": traceback.format_exc()})

def booking_index(request):
    places_dict = []
    
    ## get all the places
    places = PlekType.objects.all()
    
    # get the price of the places
    ## get the current date and time
    now = datetime.datetime.now()
    
    ## loop trough all the places and request the price at the current time
    for place in places:
        price = Price.objects.filter(startDateTime__lte=now, endDateTime__gte=now, PlekType = place).first()
        if price:
            places_dict.append({
                'id': place.id,
                'name': place.name,
                'price': price.price,
            })
    
    context = {
        'plekType': places_dict
    }
    
    return render(request, 'boer/booking/booking_index.html', context)

def confirm_booking(request):
    return render(request, 'boer/confirmation/confirmation.html')

def beschikbaarheidsCheck(request):
    # Respond only to POST requests
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "This is not a POST request."})

    try:
        start = request.POST['startDate']
        end = request.POST['endDate']

        # Get the IDs of all booked CampingSpots within the specified date range
        booked_place_ids = Booking.objects.filter(
            Q(start_date__lte=end, end_date__gte=start)
        ).values_list('CampingSpot__id', flat=True)
        
        # remove all the None values
        booked_place_ids = [x for x in booked_place_ids if x is not None]

        # Get all available CampingSpots excluding the booked ones
        available_spots = CampingSpot.objects.exclude(id__in=booked_place_ids)

        # Prepare the list of available PlekTypes
        available_places_dict = []
        for place in available_spots.distinct('plekType').values('plekType', 'plekType__name'):
            price = Price.objects.filter(
                startDateTime__lte=start, endDateTime__gte=end, PlekType_id=place['plekType']
            ).first()
            available_places_dict.append({
                'id': place['plekType'],
                'name': place['plekType__name'],
                'price': price.price if price else None
            })

        return JsonResponse({"status": "success", "available_places": available_places_dict, 'booked_place_ids': list(booked_place_ids)})

    except Exception as e:
        # Log the error if needed
        return JsonResponse({"status": "error", "message": str(e), "traceback": traceback.format_exc()})