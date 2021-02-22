from django import template


register = template.Library()

@register.filter(name="duration")
def duration(td):
    total_seconds = int(td.total_seconds())
    # hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    milliseconds = td.microseconds // 10000
    return '{:02d}\'{:02d}\"{:02d}'.format(minutes, seconds, milliseconds)