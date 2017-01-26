from django.core.exceptions import \
  ImproperlyConfigured
from django.template import (
  Library, TemplateSyntaxError)

register = Library()


@register.inclusion_tag(
  'core/includes/house_list.html',
  takes_context=True)
def house_list(context, *args, **kwargs):
    houses = (args[0] if len(args) > 0
              else kwargs.get('houses'))
    can_edit = (args[1] if len(args) > 1
          else kwargs.get('can_edit'))

    if houses is None:
        raise TemplateSyntaxError(
          "form template tag requires "
          "at least one argument: houses, "
          "which is a list.")

    return {
        'houses': houses,
        'can_edit': can_edit
    }
