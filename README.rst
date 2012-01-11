django-paginator
================

A simple paginator tag and util

Installation
------------

# Add the `paginator` directory to your Python path.
# Add `'django.core.context_processors.request'` in `settings.TEMPLATE_CONTEXT_PROCESSORS`

Usages
------

#. In template
   example

        {% load paginator %}
        {% paginate object_list %}
        {% paginator_nav %}
        <ul>
        {% for obj in object_list %}
            <li>{{ obj }}</li>
        {% endfor %}
        </ul>
        {% paginator_nav %}

#. In views

   views.py

        from django.views.generic.simple import direct_to_template
        from paginator import paginate

        def example(request):
            object_list = [{'item': i} for i in xrange(1, 100)]
            paginator, object_list = paginate(object_list, request)

            return direct_to_template(request, 'example.html',
                    {'object_list': object_list, 'paginator': paginator})

    example.html

        {% paginator_nav paginator %}
        <ul>
        {% for obj in object_list %}
            <li>{{ obj }}</li>
        {% endfor %}
        </ul>
        {% paginator_nav paginator%}
