from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Contact


def generate_report(contact):
    # Отримати дані контакту
    name = contact.name
    email = contact.email
    phone = contact.phone
    website = contact.user_website
    message = contact.message

    # Генерувати звіт
    report = f"Contact Information:\n\n"
    report += f"Name: {name}\n"
    report += f"Email: {email}\n"
    report += f"Phone: {phone}\n"
    report += f"Website: {website}\n"
    report += f"Message: {message}\n\n"

    return report


@shared_task
def send_contact_email():
    contacts = Contact.objects.filter(is_report_sent=False)

    for contact in contacts:
        # Отримати та відправити звіт
        report = generate_report(contact)
        send_mail(
            'Звіт',
            report,
            settings.EMAIL_HOST_USER,
            ['qwertyn121qwe@gmail.com'],
            fail_silently=False,
        )
        # Оновити позначку про надсилання звіту
        contact.is_report_sent = True
        contact.save()
