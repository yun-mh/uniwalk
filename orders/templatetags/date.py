import datetime
from django.template import Library


register = Library()


@register.simple_tag
def a_week_after(format):
    new_date = datetime.date.today() + datetime.timedelta(days=7)
    return new_date.strftime(format)
