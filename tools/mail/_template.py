import string
import os

def generate_body_from_template(map_parameters, template_path):
    content = open(template_path).read()
    return content.format(**map_parameters)