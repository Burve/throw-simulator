from django import template

register = template.Library()

@register.filter(name='add_bootstrap')
def add_bootstrap(field):
    return field.as_widget(attrs={
        'class': 'form-control'
    })
