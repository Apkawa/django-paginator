# -*- coding: utf-8 -*-
import re
import urllib
from django import template
register = template.Library()

from paginator.forms import PerPageForm
from paginator.utils import get_format_page_range, paginate


@register.inclusion_tag('paginator/paginator_tag.html', takes_context=True)
def paginator_nav(context, paginator=None):
    if not paginator:
        paginator = context['paginator']
    request = context['request']
    per_page_form = PerPageForm(data=request.GET)
    format_range = list(get_format_page_range(paginator.number,
            paginator.paginator.num_pages))
    return {'request': request,
            'paginator': paginator,
            'context': context,
            'format_range': format_range,
            'per_page_form': per_page_form,
            }


class PaginateNode(template.Node):
    def __init__(self, objects_list, per_page, var_name):
        self.objects_list_name = objects_list
        self.objects_list = template.Variable(objects_list)
        #TODO: move to settings
        self.per_page = int(per_page) if per_page else 6
        self.var_name = var_name if var_name else 'paginator'

    def render(self, context):
        request = context['request']
        objects_list = self.objects_list.resolve(context)
        paginated_obj, queryset = paginate(objects_list, request=request, per_page=self.per_page)
        context[self.objects_list_name] = queryset
        context[self.var_name] = paginated_obj
        return ''


@register.tag(name="paginate")
def paginate_tag(parser, token):
    '''
    {% paginate objects_list [per_page] [as name] %}
    '''
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    match = re.search(r'(?P<objects_list>[\w]+)(?: (?P<per_page>[\d]+)|)(?: as (?P<var_name>[\w]+)|)', arg)
    if not match:
        raise template.TemplateSyntaxError, \
                "%r tag has invalid arguments.\n Example: %s" % (tag_name, paginate.__doc__)
    kwargs = match.groupdict()
    return PaginateNode(**kwargs)


@register.inclusion_tag('paginator/get_append_tag.html', takes_context=True)
def get_append(context, key, val):
    '''
    {% get_append "page" 1 %} ->
    '''
    request = context['request']
    if request.GET:
        get = request.GET.copy()
        get.__setitem__(key, val)
        get_str = get.urlencode()
    else:
        get_str = urllib.urlencode({key: val})
    return {'get_str': get_str}
