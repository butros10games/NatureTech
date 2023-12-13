import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker  # Install faker using: pip install faker
from booking_system.models import Booking, Customer
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates 10 dummy bookings with random names for testing purposes'

    def handle(self, *args, **kwargs):
        fake = Faker('nl_NL')

        for _ in range(50):
            # Dummy data
            first_name = fake.first_name()
            last_name = fake.last_name()
            phone_number = fake.phone_number()[:15]  # Truncate to fit into the database field
            adults = random.randint(1, 4)
            children = random.randint(0, 2)
            email = fake.email()
            start_date = timezone.now().date() + timezone.timedelta(days=random.randint(1, 30))  # Vary check-in date within 30 days
            end_date = start_date + timezone.timedelta(days=random.randint(1, 14))  # Vary check-out date within 14 days


            # Create or get user
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.username = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()

            # Now, try to get the customer using the user
            customer, created = Customer.objects.get_or_create(user=user, defaults={'phone_number': phone_number})


            # Create booking
            booking, created = Booking.objects.get_or_create(
                customer=customer,
                age_above=adults,
                age_below=children,
                start_date=start_date,
                end_date=end_date
            )

            # Display information
            if created:
                self.stdout.write(self.style.SUCCESS(f'Dummy booking {_ + 1} created successfully!'))
                self.stdout.write(f'Order Number: {booking.order_number}')
                self.stdout.write(f'Start Date: {booking.start_date}')
                self.stdout.write(f'End Date: {booking.end_date}')
            else:
                self.stdout.write(self.style.WARNING(f'Dummy booking {_ + 1} already exists. No changes made.'))
