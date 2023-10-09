import os
import sys
import random
import zipfile
import uuid
import traceback
from datetime import date, datetime
from urllib.parse import urlparse
from math import sin, cos, sqrt, atan2, radians
import xhtml2pdf.pisa as pisa
from io import BytesIO

from django.template import loader
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from portfolio import settings


def generate_pdf(request, template_name, context, file_name, unique_name):
    result = False
    message = 'Error'
    form_data = dict()
    try:

        import subprocess
        template = loader.get_template(template_name)
        html = template.render(context)

        source_html_path = os.path.join(settings.BASE_DIR, 'templates',  "resume_template_01.html")
        output_pdf_path = os.path.join(settings.BASE_DIR, 'templates', "{first_name}_{last_name}_{designation}.pdf" % (context['first_name'], context['last_name'], context['designation']))
        with open(source_html_path, 'w') as resume:
            resume.write(html)

        cmd = "xhtml2pdf --css={0} {1} {2}".format(source_html_path, output_pdf_path)
        p = subprocess.call(cmd, shell=True)

        with open(output_pdf_path, 'rb') as po_pdf:
            folder_path = "templates"
            file_path = "%s/%s" % (folder_path, file_name)
            file_url = default_storage.save(file_path, ContentFile(po_pdf.read()))
            form_data['url'] = file_url

        if os.path.exists(source_html_path):
            os.remove(source_html_path)
        
        if os.path.exists(output_pdf_path):
            os.remove(output_pdf_path)
        
        message = 'Success'
        result = True
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
    return result, message, form_data