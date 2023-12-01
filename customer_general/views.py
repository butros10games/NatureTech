import http
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import BtIpAdress
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'customer_general/index.html')

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

        messages.success(request, 'Uw vraag is verstuurd!')

    return render(request, 'customer_general/contact.html')

def ip_logger(request, ip_adress):
    BtIpAdress.objects.create(ip_adress=ip_adress)
    
    return HttpResponse(status=http.HTTPStatus.OK) # 200 OK

def ip_adress_display(request):
    ## Make it so that only the last 10 ip adresses are displayed and the newest one is on top
    ip_adresses = BtIpAdress.objects.all().order_by('-date')[:10]

    context = {
        "ip_adresses": ip_adresses
    }

    return render(request, 'customer_general/ip_adress_display.html', context=context)