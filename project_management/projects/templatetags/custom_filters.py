from django import template

register = template.Library()

@register.filter
def status_class(status):
    status_classes = {
        'todo': 'primary',
        'in_progress': 'warning',
        'done': 'success'
    }
    return status_classes.get(status, 'secondary')

@register.filter
def priority_class(priority):
    priority_classes = {
        'low': 'info',
        'medium': 'primary',
        'high': 'danger'
    }
    return priority_classes.get(priority, 'secondary')
