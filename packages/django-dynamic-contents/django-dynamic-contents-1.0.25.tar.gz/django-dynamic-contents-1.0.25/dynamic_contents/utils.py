# dynamic_content_utils.py

import re
from django.utils.translation import get_language

# Assuming the existence of get_text, get_i18n, get_html from the previous answer
# Add the following new utility functions

def generate_text(format, parts):
    """
    Generates text from a format and parts.
    """
    format_string = format.get_content()
    if not format_string:
        return ''

    for part in parts:
        format_string = format_string.replace("{{" + part.field + "}}", part.get_content() or '')
    return format_string


def generate_i18n(format, parts):
    """
    Generates internationalized text from a format and parts.
    """
    format_string = format.get_content()
    if not format_string:
        return ''

    placeholders = re.findall(r'\{\{(\w+)\}\}', format_string)
    index_map = {placeholder: idx for idx, placeholder in enumerate(placeholders)}

    for part in parts:
        if part.field in index_map:
            idx = index_map[part.field]
            replacement = f'<{idx}>{part.get_content()}</{idx}>'
            placeholder = f"{{{{{part.field}}}}}"
            format_string = format_string.replace(placeholder, replacement, 1)
    return format_string


def generate_html(format, parts):
    """
    Generates HTML content from a format and parts.
    """
    format_string = format.get_content()
    if not format_string:
        return ''

    for part in parts:
        link = part.link or '#'
        replacement = f'<a class="{part.field}" href="{link}">{part.get_content()}</a>'
        placeholder = f"{{{{{part.field}}}}}"
        format_string = format_string.replace(placeholder, replacement)
    return format_string