from django.core.mail import send_mail

def sendmail():
    """
    Sending mail on subscribers
    """
    send_mail(
        'Test Subject',
        'Here is the message we want.',
        'fromdjango@example.com',
        ['toconsolelog@example.com'],
        fail_silently=False,
    )
