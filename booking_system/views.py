from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.core.mail import send_mail


def booking_form(request):
    return render(request, 'booking_form.html')

def confirm_booking(request):
    if request.method == 'POST':
        FirstName = request.POST['FirstName']
        LastName = request.POST['LastName']
        NumberofGuests = request.POST['NumberofGuests']
        mail = request.POST['CustomerEmail']
        Start = request.POST['Start']
        End = request.POST['End']

        send_mail(
              'Boekings bevestiging',
            f'Dankuwel, {FirstName} {LastName}, voor het reserveren van een kampeerplek op de boerencamping van {Start} tot {End}.',
            'bobelsendoorn@gmail.com', 
            [mail],  
            fail_silently=False,
        )
        return render(request, 'confirmation.html', {'name': FirstName, 'mail': CustomerEmail, 'date': Start})
    else:
        return HttpResponseRedirect(reverse('booking_form'))

      

       