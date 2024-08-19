from django.core.mail import send_mail
import dramatiq

@dramatiq.actor
def email_user(applicant_email):
    send_mail(
                subject="Application sent successfully.",
                message="Hello, your application has been sent to the selected hostels.",
                from_email="groupfiftyeight95@gmail.com",
                recipient_list=[applicant_email],
                fail_silently=False
            )