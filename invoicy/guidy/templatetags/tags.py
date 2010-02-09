from django import template
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
import re
register = template.Library()

@register.simple_tag
def link(request, url, text):
    ret = "<a href='%s' class='%s'>%s</a>"
    if re.search('^' + url + '$', request.path):
        return ret %(url, 'current_link', _(text))
    return ret %(url, '', _(text))
