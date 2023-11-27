from django.shortcuts import render, redirect
from django.core.mail import send_mail


def booking_form(request):
    if request.method == 'POST':
        first_name = request.POST['FirstName']
        last_name = request.POST['LastName']
        number_of_guests = request.POST['NumberofGuests']
        mail = request.POST['CustomerEmail']
        start = request.POST['StartDate']
        end = request.POST['EndDate']

        send_mail(
              'Boekings bevestiging',
            f'Dankuwel, {first_name} {last_name}, voor het reserveren van een kampeerplek op de boerencamping voor {number_of_guests} personen van {start} tot {end}.',
            {mail},
            [mail],  
            fail_silently=False,
        )
        return redirect('confirm_booking')
    return render(request, 'booking/booking_form.html')

def confirm_booking(request):
    return render(request, 'confirmation/confirmation.html')

      

       