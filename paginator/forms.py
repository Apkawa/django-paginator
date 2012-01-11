from django import forms
from django.conf import settings

PAGINATOR_PER_PAGE_CHOICES = getattr(settings, "PAGINATOR_PER_PAGE_CHOICES", [25, 50, 100])


class PerPageForm(forms.Form):
    per_page = forms.ChoiceField(
            choices=((p, str(p)) for p in PAGINATOR_PER_PAGE_CHOICES),
            required=False)
