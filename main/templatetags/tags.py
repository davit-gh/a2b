from django import template
register = template.Library()

@register.inclusion_tag("main/includes/form_errors.html", takes_context=True)
def errors_for(context, form):
    """
    Renders an alert if the form has any errors.
    """
    context["form"] = form
    return context

