from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """ Returns true if user belongs to given group_name """
    return user.groups.filter(name=group_name).exists()
