from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    템플릿에서 딕셔너리 키와 변수를 사용하여 값에 접근할 수 있게 해주는 필터.
    예: {{ my_dict|get_item:my_variable }}
    """
    return dictionary.get(key)
