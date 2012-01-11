# -*- coding: utf-8 -*-
from django.views.generic.simple import direct_to_template

from paginator import paginate


def example_1(request):
    object_list = [{'item': i} for i in xrange(1, 100)]
    return direct_to_template(request, 'paginator_example_1.html',
                {'object_list': object_list})


def example_2(request):
    object_list = [{'item': i} for i in xrange(1, 100)]
    paginator, object_list = paginate(object_list, request)

    return direct_to_template(request, 'paginator_example_2.html',
            {'object_list': object_list, 'paginator': paginator})
