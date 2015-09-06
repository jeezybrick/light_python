from django.forms.widgets import SelectMultiple, Select
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class MyWidgetForColor(Select):
    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html('<option style="background-color:{}" value="{}"{}></option>',
                           force_text(option_label),
                           option_value,
                           selected_html)


class MyWidgetForLabels(SelectMultiple):
    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html('<option data-img-src="/static/notes/labels/default/{}" value="{}"{}>{}</option>',
                           force_text(option_label),
                           option_value,
                           selected_html,
                           force_text(option_label))