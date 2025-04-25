from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

# @shared_task
# def send_welcome_email(email,username):
#     subject = 'WELCOME MAIL'
#     message = f'Welcome {username} to our website!'
#     from_mail = settings.EMAIL_HOST_USER
#     send_mail(subject,message,from_mail,[email])
@shared_task
def send_welcome_email(email, username):
    from django.core.mail import send_mail
    from django.conf import settings
    import logging

    try:
        subject = 'WELCOME MAIL'
        message = f'Welcome {username} to our website!'
        from_email = settings.EMAIL_HOST_USER
        print(f"Sending email to {email}...")

        result = send_mail(subject, message, from_email, [email])
        print(f"Send mail result: {result}") 

        if result == 1:
            print("✅ Email sent successfully via Celery!")
        else:
            print("❌ Celery tried but didn't send mail.")

    except Exception as e:
        print(f"🚨 Exception: {e}")
        logging.error(f"Email sending failed: {e}")
