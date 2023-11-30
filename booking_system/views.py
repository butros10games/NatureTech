from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Booking, Customer, Notes
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def booking_form(request):
    if request.method == 'POST':
        first_name = request.POST['FirstName']
        last_name = request.POST['LastName']
        number_of_guests = request.POST['NumberofGuests']
        mail = request.POST['CustomerEmail']
        start = request.POST['StartDate']
        end = request.POST['EndDate']

        user, created = User.objects.get_or_create(email=mail)
        if created:
            user.username = mail
            user.first_name = first_name
            user.last_name = last_name
            user.save()

        customer, created = Customer.objects.get_or_create(user=user)
        booking, created = Booking.objects.create(customer=customer, age_above=number_of_guests, start_date=start, end_date=end)
        
        ## reload booking out of the database
        booking.refresh_from_db()

        context = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_arrival": start,
            "date_of_departure": end,
            "accomodation": end,
            "order_number": booking.order_number,
            "price": end,
            "method_of_paying": end
        }

        html_message = render_to_string("booking/confirmation_mail.html", context=context)
        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
        subject = 'Bevestiging voor uw reservering op Camping de Groene Weide', 
        body = plain_message,
        from_email = None ,
        to= {mail}
            )

        message.attach_alternative(html_message, "text/html")
        message.send()

        messages.success(request,f'Dankuwel, {first_name} {last_name}, voor het reserveren van een kampeerplek van {start} tot {end}. Een bevestigingsmail is verstuurd naar {mail}!')

        return redirect('confirm_booking')
    return render(request, 'booking/booking_index.html')

def confirm_booking(request):
    return render(request, 'confirmation/confirmation.html')

def contact_form(request):
    if request.method == 'POST':
         first_name = request.POST['first_name']
         last_name = request.POST['last_name']
         mail = request.POST['email']
         phone_number = request.POST['phone_number']
         contact_message = request.POST['contact_message']

    context = {
            "first_name": first_name,
            "last_name": last_name,
            "email": mail,
            "phone_number": phone_number,
            "contact_message": contact_message
        }
    
    html_message = render_to_string("mail/contact_confirmation_mail.html", context=context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
    subject = 'Uw vraag is ontvangen', 
    body = plain_message,
    from_email = None ,
    to= {mail}
    )
    message.attach_alternative(html_message, "text/html")
    message.send()

    messages.succes(request, 'Uw vraag is verstuurd!')

    return render(request, 'customer_general/contact.html')

    
    




      

       