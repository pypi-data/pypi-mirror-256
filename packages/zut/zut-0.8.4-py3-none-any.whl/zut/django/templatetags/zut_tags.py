from __future__ import annotations
import logging
import re
from django import template
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.conf import settings

logger = logging.getLogger(__name__)

register = template.Library()

# avoid logging warnings for every request
_missing_version: list[str] = []
_missing_integrity: list[str] = []

def _get_lib_url(package, file, version=None, prefix=None):
    LOCAL_STATIC_LIB = getattr(settings, "LOCAL_STATIC_LIB", False)
    if LOCAL_STATIC_LIB:
        return f"{static(LOCAL_STATIC_LIB if isinstance(LOCAL_STATIC_LIB, str) else 'lib')}/{package}/{file}"
    else:
        if version:
            return f"https://cdn.jsdelivr.net/npm/{package}@{version}/{file}"
        else:
            return f"https://cdn.jsdelivr.net/npm/{package}/{file}"


@register.simple_tag
def style_lib(package, file, version=None, integrity=None):
    """
    Usage example in Django base template:

        {% load static %}
        {% load static_lib %}
        ...
        <head>
        ...
        {% style_lib  'bootstrap' 'dist/css/bootstrap.min.css' '5.2.0' 'sha256-7ZWbZUAi97rkirk4DcEp4GWDPkWpRMcNaEyXGsNXjLg=' %}
        ...
        </head>
    """
    if file and version and re.match(r'^\d+', file):
        # invert
        arg2 = file
        file = version
        version = arg2

    url = _get_lib_url(package, file, version)

    if not version and not url in _missing_version:
        logger.warning(f"missing version for style_lib: {url}")
        _missing_version.append(url)
        
    html = f"<link rel=\"stylesheet\" href=\"{url}\""
    
    if integrity:
        html += f" integrity=\"{integrity}\" crossorigin=\"anonymous\""
    else:
        logger.warning(f"missing integrity hash for style_lib: {url}")
        _missing_integrity.append(url)

    html += f" />"
    return mark_safe(html)


@register.simple_tag
def script_lib(package, file, version=None, integrity=None, defer=False):
    """
    Usage example in Django base template:

        {% load static %}
        {% load static_lib %}
        ...
        <head>
        ...
        {% script_lib 'bootstrap' 'dist/js/bootstrap.bundle.min.js' '5.2.0' 'sha256-wMCQIK229gKxbUg3QWa544ypI4OoFlC2qQl8Q8xD8x8=' %}
        ...
        </head>
    """
    if file and version and re.match(r'^\d+', file):
        # invert
        arg2 = file
        file = version
        version = arg2
    
    url = _get_lib_url(package, file, version)
    
    if not version and not url in _missing_version:
        logger.warning(f"missing version for script_lib: {url}")
        _missing_version.append(url)

    html = f"<script"
    if defer:
        html=" defer"
    html += f" src=\"{url}\""
    
    if integrity:
        html += f" integrity=\"{integrity}\" crossorigin=\"anonymous\""
    elif not url in _missing_integrity:
        logger.warning(f"missing integrity hash for script_lib: {url}")
        _missing_integrity.append(url)

    html += f"></script>"
    return mark_safe(html)


@register.simple_tag
def style_min(name: str):
    if m := re.match(r'^([a-z0-9_]+)\:(.+)$', name, re.IGNORECASE):
        name = f"{m[1]}/pages/{m[2]}"
    
    if not name.endswith('.css'):
        name += '.css'
    
    if not settings.DEBUG:
        if not name.endswith('.min.css'):
            name = re.sub(r'(.css)$', '.min.css', name)
    
    return mark_safe(f'<link rel="stylesheet" href="{static(name)}" />')


@register.simple_tag
def script_min(name: str):
    if m := re.match(r'^([a-z0-9_]+)\:(.+)$', name, re.IGNORECASE):
        name = f"{m[1]}/pages/{m[2]}"
    
    if not name.endswith('.js'):
        name += '.js'
    
    if not settings.DEBUG:
        if not name.endswith('.min.js'):
            name = re.sub(r'(.js)$', '.min.js', name)

    return mark_safe(f'<script type="module">import "{static(name)}";</script>')
