from __future__ import annotations

import os
from pathlib import Path
import pathlib
from pprint import pprint

from jinja2 import Environment, BaseLoader
from colorama import Fore, Back, Style


ls_tmpl = """
{%- for type, values in config.items() %}
    {{- Style.BRIGHT }}{{- type.upper() }}{{ Style.NORMAL }}
    {% for value in values %}
    {{ value }}
{% endfor -%}
{%- endfor -%}
"""

def prepare_config(config: dict) -> str:
    """

    :param config:
    :return: str
    """
    rtmpl = Environment(keep_trailing_newline=False, trim_blocks=True, lstrip_blocks=True, loader=BaseLoader()).from_string(ls_tmpl)
    return rtmpl.render(config=config, Style=Style, Fore=Fore, Back=Back)


def squish_info(config) -> dict:
    info = config
    info_dict = {}
    pprint(config)
    for k, v, in info.items():
        info_dict[k] = {}
        for k2 in v:
            pprint(k2)
            info_dict[k][k2] = {}

    return info_dict

    # check if path exists
def path_validation(path: str | os.PathLike | Path) -> bool:
    """

    :param path:
    :return: True
    """
    return Path.exists(path, follow_symlinks=True)

# if it doesn't, create it
def path_create(path: str | os.PathLike | Path) -> bool:
    """

    :param path:
    :return: True
    """
    if path_validation(path):
        return False
    else:
        Path.mkdir(path, parents=True, exist_ok=True)
