from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from bp import settings as bp_settings
from django.utils.html import strip_tags
import sys, traceback

def send_email(  from_email = bp_settings.EMAIL_FROM_ADDRESS,
                to=[bp_settings.SERVER_MAIL], 
                cc=[],
                subject="Automatic generated email",
                text_message="Email generated automatically! Please don't reply to this mail.", 
                html_template_file="generic.html",
                html_context={},
                file_paths=[]):
    try:
        html_template_path = "email/" + html_template_file

        email = EmailMultiAlternatives(
                subject=subject,
                body=text_message,
                from_email=from_email,
                to=to,
                cc=cc
        )

        if len(html_context) > 0:
            html_content = render_to_string(html_template_path, context=html_context)
            email.attach_alternative(html_content, "text/html")

        for file_path in file_paths:
            email.attach_file(file_path)

        email.send()
        return True
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        return False
        
        