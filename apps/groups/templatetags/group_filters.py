from django import template

register = template.Library()

@register.filter
def get_membership_field(form, membership_id):
    """
    Template filter to get the field for a specific membership role.
    
    Usage: {{ form|get_membership_field:membership.id }}
    """
    field_name = f'membership_{membership_id}_role'
    if field_name in form.fields:
        return form[field_name]
    return ''
