from django.core.mail import EmailMessage


def send_mail(to_email, confirmation_code):
    mail_subject = 'Activation link has been sent to your email id'
    message = confirmation_code
    email = EmailMessage(mail_subject,
                         message,
                         to=[to_email])
    print(to_email)
    email.send()
