from django_ratelimit.decorators import ratelimit

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Booking, Customer


@ratelimit(key="ip", rate="3/60m")  # Limit to 5 requests per 15 minutes per IP address
def booking_form(request):
    if getattr(request, "limited", False):
        return JsonResponse(
            {
                "status": "error",
                "type": "rate_limit",
                "message": "You have exceeded the rate limit. Please wait before trying again.",
            }
        )

    if request.method == "POST":
        try:
            first_name = request.POST["firstName"]
            last_name = request.POST["lastName"]
            phone_number = request.POST["phone"]
            adults = request.POST["adults"]
            childeren = request.POST["children"]
            mail = request.POST["email"]
            start = request.POST["startDate"]
            end = request.POST["endDate"]

            user, created = User.objects.get_or_create(email=mail)
            if created:
                user.username = mail
                user.first_name = first_name
                user.last_name = last_name
                user.save()

            customer, created = Customer.objects.get_or_create(
                user=user, phone_number=phone_number
            )
            booking_created = Booking.objects.create(
                customer=customer,
                age_above=adults,
                age_below=childeren,
                start_date=start,
                end_date=end,
            )
            booking = booking_created if isinstance(booking_created, Booking) else None
            created = True  # Assuming the object is always created in this context

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
                "method_of_paying": end,
                "adults": adults,
                "children": childeren,
            }

            html_message = render_to_string(
                "boer/booking/confirmation_mail.html", context=context
            )
            plain_message = strip_tags(html_message)

            message = EmailMultiAlternatives(
                subject="Bevestiging voor uw reservering op Camping de Groene Weide",
                body=plain_message,
                from_email=None,
                to={mail},
            )

            message.attach_alternative(html_message, "text/html")
            message.send()

            # Second email to the specified email address
            html_message_admin = render_to_string(
                "boer/booking/confirmation_mail_admin.html", context=context
            )
            plain_message_admin = strip_tags(html_message_admin)

            message_admin = EmailMultiAlternatives(
                subject="Nieuwe boeking ontvangen",
                body=plain_message_admin,
                from_email=mail,  # Use your default email address or specify one
                to=[settings.DEFAULT_FROM_EMAIL],  # Use a list for the 'to' parameter
            )
            message_admin.attach_alternative(html_message_admin, "text/html")
            message_admin.send()

            messages.success(
                request,
                f"Dankuwel, {first_name} {last_name}, voor het reserveren van een kampeerplek van {start} tot {end}. Een bevestigingsmail is verstuurd naar {mail}!",
            )

            return JsonResponse({"status": "success"})

        except Exception as e:
            # Log the error if needed
            return JsonResponse({"status": "error", "message": str(e)})


def booking_index(request):
    return render(request, "boer/booking/booking_index.html")


def confirm_booking(request):
    return render(request, "boer/confirmation/confirmation.html")
