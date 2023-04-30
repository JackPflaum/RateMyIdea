from django import template

register = template.Library()

@register.filter
def is_numeric(value):
    """Custom template filter to check if value is numeric.
    First, check whether value can be converted to float.
    If it is numeriic than return True otherwise return False."""
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False
