# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings

PAGINATOR_PER_PAGE = getattr(settings, "PAGINATOR_PER_PAGE", 25)


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
            per_page = int(request.GET.get("per_page", PAGINATOR_PER_PAGE))
        except ValueError:
            pass

    per_page = per_page or PAGINATOR_PER_PAGE

    paginator = Paginator(list_obj, per_page)
    try:
        paginated_obj = paginator.page(page)
    except (EmptyPage, InvalidPage):
        paginated_obj = paginator.page(paginator.num_pages)
    return paginated_obj, paginated_obj.object_list


def get_format_page_range(num_page, total_pages):
    # FIXME доработать
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
