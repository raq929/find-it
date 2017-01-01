from django.core.exceptions import \
  ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.template import (
  Library, TemplateSyntaxError)

register = Library()

@register.inclusion_tag(
  'core/includes/confirm_delete.html',
  takes_context=True)
def delete(context, *args, **kwargs):
  obj = (args[0] if len(args) > 0
          else kwargs.get('obj'))
  children = (args[1] if len(args) > 1
          else kwargs.get('children'))
  children_name = (args[2] if len(args) > 2
          else kwargs.get('children_name'))
  button = (args[3] if len(args) > 3
          else kwargs.get('button'))
  parent = (args[4] if len(args) > 4
          else kwargs.get('parent'))


  if obj is None:
    raise TemplateSyntaxError(
      "form template tag requires "
      "at least one argument: obj. "
      "which is a model instance with "
      "a name property.")

  return {
    'obj': obj,
    'children': children,
    'children_name': children_name,
    'button': button,
    'parent': parent,
  }
