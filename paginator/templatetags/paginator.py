# -*- coding: utf-8 -*-
import re
import urllib

from django import template
register = template.Library()

from django.core.paginator import Paginator, InvalidPage, EmptyPage

from django import forms


PER_PAGE = [25, 50, 100]
PER_PAGE_CHOICES = ((p, str(p)) for p in PER_PAGE)
DEFAULT_PER_PAGE = 25


class PerPageForm(forms.Form):
    per_page = forms.ChoiceField(choices=PER_PAGE_CHOICES, required=False)


def paginate(list_obj, request=None, per_page=None, page=1):
    '''
    return paginator, paginate_list
    '''
    if request:
        try:
            page = int(request.GET.get("page", "1"))
        except ValueError:
            page = 1

        try:
            per_page = int(request.GET.get("per_page", DEFAULT_PER_PAGE))
        except ValueError:
            pass

    per_page = per_page or DEFAULT_PER_PAGE

    paginator = Paginator(list_obj, per_page)
    try:
        paginated_obj = paginator.page(page)
    except (EmptyPage, InvalidPage):
        paginated_obj = paginator.page(paginator.num_pages)
    return paginated_obj, paginated_obj.object_list


def get_format_page_range(num_page, total_pages):
    #FIXME доработать
    page_range = range(1, total_pages + 1)
    if len(page_range) < 9:
        return page_range
    begin_range = page_range[:3]
    end_range = page_range[-3:]
    position_range = page_range[num_page - 1 if num_page == 1 else num_page - 2: num_page + 1]
    space = [None]
    if set(position_range) & (set(begin_range) | set(end_range)):
        if set(position_range) & set(begin_range):
            format_page_range = list(set(begin_range) | set(position_range)) + space + end_range[-1:]
        elif set(end_range) & set(position_range):
            format_page_range = begin_range[:1] + space + list(set(position_range) | set(end_range))
    else:
        format_page_range = begin_range[:1] \
                            + space \
                            + position_range \
                            + space \
                            + end_range[-1:]
    return format_page_range


@register.inclusion_tag('paginator_tag.html', takes_context=True)
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


@register.inclusion_tag('get_append_tag.html', takes_context=True)
def get_append(context, key, val):
    request = context['request']
    if request.GET:
        get = request.GET.copy()
        get.__setitem__(key, val)
        get_str = get.urlencode()
    else:
        get_str = urllib.urlencode({key: val})
    return {'get_str': get_str}
