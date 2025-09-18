from django import template
from django.template.defaultfilters import floatformat

register = template.Library()

@register.filter
def rupee_format(value):
    """
    Format a number as Indian currency with rupee symbol and proper comma formatting
    """
    if value is None:
        return "₹0"
    
    try:
        # Convert to float and format with commas
        float_value = float(value)
        formatted_value = "{:,.0f}".format(float_value)
        return f"₹{formatted_value}"
    except (ValueError, TypeError):
        return "₹0"

@register.filter
def rupee_format_decimal(value, decimal_places=2):
    """
    Format a number as Indian currency with decimal places
    """
    if value is None:
        return "₹0.00"
    
    try:
        # Convert to float and format with commas and decimals
        float_value = float(value)
        formatted_value = "{:,.2f}".format(float_value)
        return f"₹{formatted_value}"
    except (ValueError, TypeError):
        return "₹0.00"
