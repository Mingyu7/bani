from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    템플릿에서 딕셔너리 키와 변수를 사용하여 값에 접근할 수 있게 해주는 필터.
    예: {{ my_dict|get_item:my_variable }}
    """
    return dictionary.get(key)

@register.filter
def meal_replace(value, arg):
    """
    String replace filter for meal plan menu text.
    Usage: {{ value|meal_replace:"old,new" }}
    """
    if not isinstance(value, str):
        return value
    
    try:
        old, new = arg.split(',')
    except ValueError:
        return value # Return original value if arg is not in 'old,new' format
    
    return mark_safe(value.replace(old, new))
