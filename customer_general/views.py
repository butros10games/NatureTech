import http
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django_ratelimit.decorators import ratelimit

from .models import BtIpAdress, BtnState
from django.http import HttpResponse
from django.conf import settings

# Create your views here.
def index(request):
    return render(request, 'boer/customer_general/index.html')

@ratelimit(key='ip', rate='5/60m')  # Limit to 5 requests per 15 minutes per IP address
def contact(request):
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
      
        html_message_user = render_to_string("boer/mail/contact_confirmation_mail.html", context=context)
        plain_message_user = strip_tags(html_message_user)

        message_user = EmailMultiAlternatives(
            subject='Uw vraag is ontvangen',
            body=plain_message_user,
            from_email=settings.DEFAULT_FROM_EMAIL,  # Use your default email address or specify one
            to=[mail],  # Use a list for the 'to' parameter
        )
        message_user.attach_alternative(html_message_user, "text/html")
        message_user.send()

        # Second email to the specified email address
        html_message_admin = render_to_string("boer/mail/new_request_mail.html", context=context)
        plain_message_admin = strip_tags(html_message_admin)

        message_admin = EmailMultiAlternatives(
            subject='Nieuwe vraag ontvangen',
            body=plain_message_admin,
            from_email=mail,  # Use your default email address or specify one
            to=[settings.DEFAULT_FROM_EMAIL],  # Use a list for the 'to' parameter
        )
        message_admin.attach_alternative(html_message_admin, "text/html")
        message_admin.send()

        messages.success(request, 'Uw vraag is verstuurd!')

    return render(request, 'boer/customer_general/contact.html')

def faciliteiten(request):
    return render(request, 'boer/customer_general/faciliteiten.html')

def nieuws(request):
    return render(request, 'boer/customer_general/nieuws.html')

def ip_logger(request, ip_adress):
    BtIpAdress.objects.create(ip_adress=ip_adress)
    
    return HttpResponse(status=http.HTTPStatus.OK) # 200 OK

def ip_adress_display(request):
    ## Make it so that only the last 10 ip adresses are displayed and the newest one is on top
    ip_adresses = BtIpAdress.objects.all().order_by('-date')[:10]

    context = {
        "ip_adresses": ip_adresses
    }

    return render(request, 'boer/customer_general/ip_adress_display.html', context=context)

def btn_logger(request, ip_adress, state):
    ## string to bool converter
    if state == "True":
        state = True
    elif state == "False":
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

    return render(request, 'boer/customer_general/btn_states_display.html', context=context)