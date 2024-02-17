from django import template

from django.forms import BoundField, MultipleChoiceField
from django.forms.widgets import Select
from django.core.validators import RegexValidator

from aw.model.job import BaseJobCredentials
from aw.utils.util import is_set

register = template.Library()


@register.filter
def get_form_field_attributes(bf: BoundField) -> str:
    attr_str = ''
    for key, value in bf.field.widget_attrs(bf.field.widget).items():
        attr_str += f' {key}="{value}"'

    return attr_str


@register.filter
def get_form_field_validators(bf: BoundField) -> str:
    attr_str = ''

    for validator in bf.field.validators:
        if isinstance(validator, RegexValidator):
            # pylint: disable=W0212
            # was not able to get the raw regex from regex attribute ('_lazy_re_compile')
            regex = validator._constructor_args[1]['regex']
            attr_str += f' pattern="{regex}"'
            if validator.message is not None:
                attr_str += f' title="{validator.message}"'

    return attr_str


@register.filter
def form_field_is_dropdown(bf: BoundField) -> bool:
    return isinstance(bf.field.widget, Select)


def get_form_required(bf: BoundField) -> str:
    return ' required' if bf.field.required else ''


def get_form_field_value(bf: BoundField, existing: dict) -> (str, None):
    # PWD_ATTRS are not exposed here
    if bf.name not in existing and bf.name not in BaseJobCredentials.PWD_ATTRS:
        return None

    if bf.name in BaseJobCredentials.PWD_ATTRS:
        enc_field = '_enc_' + bf.name
        if enc_field in existing and not is_set(existing[enc_field]):
            return None

        if enc_field not in existing:
            value = None

        else:
            value = BaseJobCredentials.PWD_HIDDEN

    else:
        value = str(existing[bf.name])

    return str(value)


@register.filter
def get_form_field_select(bf: BoundField, existing: dict) -> str:
    selected = None
    if bf.name in existing:
        selected = str(existing[bf.name])
    elif bf.field.initial is not None:
        selected = bf.field.initial

    options_str = f'<select class="form-control" id="{bf.id_for_label}" name="{bf.name}"'
    if isinstance(bf.field, MultipleChoiceField):
        options_str += ' multiple'
        selected = None  # not implemented

    options_str += '>'

    # pylint: disable=W0212
    for option in bf.field._choices:
        is_selected = 'selected' if str(option[0]) == str(selected) else ''
        options_str += f'<option value="{option[0]}" {is_selected}>{option[1]}</option>'

    options_str += '</select>'
    return options_str


@register.filter
def get_form_field_input(bf: BoundField, existing: dict) -> str:
    field_classes = 'form-control'
    field_attrs = f'id="{bf.id_for_label}" name="{bf.name}"'
    search_choices = ''

    field_value = ''
    value = get_form_field_value(bf, existing)
    if value is not None:
        field_value = f'value="{value}"'

    if bf.name.find('_pass') != -1:
        field_attrs += ' type="password"'

    elif bf.name.find('_file') != -1:
        field_classes += ' aw-fs-browse'
        field_attrs += (f' type="text" aw-fs-selector="{bf.name}" aw-fs-type="files"'
                        f' aw-fs-choices="aw-fs-choices-{bf.name}"')
        if value is None:
            field_attrs += 'pattern="^\\b$"'

        else:
            field_attrs += 'pattern=".*"'

        search_choices = f'<ul id="aw-fs-choices-{bf.name}"></ul>'

    return (f'<input class="{field_classes}" {field_attrs} '
            f'{field_value} {get_form_required(bf)}'
            f'{get_form_field_attributes(bf)} {get_form_field_validators(bf)}>'
            f'{search_choices}')
