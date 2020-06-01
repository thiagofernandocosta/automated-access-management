import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import mail
from mail import _template
from mail import _mail

absolute_path = path = os.path.dirname(os.path.abspath(__file__))
template_html = '/template/kube.html'
user = os.environ.get('EMAIL')

def notify():
    path_file = '{}/{}'.format(absolute_path, template_html)
    generate_template_html = _template.generate_body_from_template(dict(), path_file)
    _mail.send_mail(user, generate_template_html)

if __name__ == "__main__":
    notify()