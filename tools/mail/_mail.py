import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

username = os.environ.get('PROVIDER_EMAIL')
password = os.environ.get('PROVIDER_EMAIL_PW')

def send_mail(email_user, template_html):
    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465
    
    from_addr = username
    to_addrs = [email_user]

    # The email body for recipients with non-HTML email clients.
    # body_text = "Hello,\r\nPlease see the attached file for a list of customers to contact."

    # The HTML body of the email.
    body_html = template_html

    # Create a multipart/mixed parent container.
    message = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    message['subject'] = 'My Topic'
    message['from'] = from_addr
    message['to'] = ', '.join(to_addrs)

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')

    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    htmlpart = MIMEText(body_html , 'html')

    # Add the text and HTML parts to the child container.
    msg_body.attach(htmlpart)

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    message.attach(msg_body)

    try: 
        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        server.login(username, password)
        server.sendmail(from_addr, to_addrs, message.as_string())
    except Exception as e:
        print(e)
    finally:
        server.quit()