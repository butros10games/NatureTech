from django.shortcuts import render, redirect
from django.core.mail import send_mail


def booking_form(request):
    return render(request, 'templates/booking_form.html')

def confirm_booking(request):
    if request.method == 'POST':
        first_name = request.POST['FirstName']
        last_name = request.POST['LastName']
        number_of_guests = request.POST['NumberofGuests']
        mail = request.POST['CustomerEmail']
        start = request.POST['Start']
        end = request.POST['End']

        send_mail(
              'Boekings bevestiging',
            f'Dankuwel, {first_name} {last_name}, voor het reserveren van een kampeerplek op de boerencamping van {start} tot {end}.',
            'bobelsendoorn@gmail.com', 
            [mail],  
            fail_silently=False,
        )
        return render(request, 'confirmation.html', {'name': first_name, 'mail': mail, 'date': start})
    else:
        return redirect('booking_form')

      

       