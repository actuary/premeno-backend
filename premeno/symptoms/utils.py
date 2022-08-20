import pdfkit

from django.template.loader import get_template


def render_to_pdf(template_name: str, context : dict):
    template = get_template(template_name)
    html = template.render(context=context)
    options = {"encoding": "UTF-8"}
    return pdfkit.from_string(html, options=options)
