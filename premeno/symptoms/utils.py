import pdfkit

from django.conf import settings
from django.template.loader import get_template


def render_to_pdf(template_name: str, context : dict):
    template = get_template(template_name)
    html = template.render(context=context)
    options = {"encoding": "UTF-8"}
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF)
    return pdfkit.from_string(html, options=options, configuration=config)
