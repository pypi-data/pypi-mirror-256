"""Create an HTML from a Camp object"""

from typing import Union, Optional, List
from pathlib import Path

from ._camp import Camp
from .common.types import ColorObject, ColorSpace
from .common.validators import PathValidator
from .color_objects.color_space import BaseColor, RGB
from ._settings import settings

REPORT_TEMPLATE = """<!DOCTYPE html>
<style>
{css}
</style>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>{camp_name}</title>
        <meta name="viewport" content="width=device-width,initial-scale=1.0">
        <meta name="description" content="{description}">
        <meta name="author" content="colorcamp">
        <meta http-equiv="content-language" content="ll-cc">
    </head>
    <body>
        <div class="container">
            <section id="descriptionSection">
                <h1>{camp_name}</h1>
                <p>{description}</p>
            </section>
        </div>
        {sections_html}
    </body>
</html>
"""

SECTION_HTML = """<div class="container">
    <section id="colorNameSection">
        <ul class="colorNameList">
            <h2>{section_name}</h2>
            {content}
        </ul>
        <div class="clearfix"></div>
    </section>
</div>
"""

COLOR_HTML = """
<li>
    <h4>{name}</h4>
    <div class="color" style="background-color:{color}">&nbsp;</div>
    {spaces}
</li>
"""

SCALE_HTML = """
<li>
    <h4>{name}</h4>
    <div class="color" style="background-image: linear-gradient(to right, {grad})">&nbsp;</div>
    {spaces}
</li>
"""

MAP_HTML = """
<li>
    <h4>{name}</h4>
    {colors}
</li>
"""

MAP_COLOR_HTML = """
<div class="color" style="background-color:{color}">{text}</div>
"""

SPACE_HTML = """
<div class="space">
    <div class="name">{name}</div>
    {values}
</div>
"""


def _value_formatter(value) -> str:
    value_html = '<div class="value">{value}</div>'
    if isinstance(value, str):
        return value_html.format(value=value)
    elif isinstance(value, tuple):
        return "\n".join(
            [value_html.format(value=int(val) if isinstance(value, RGB) else f"{val:.2f}") for val in value]
        )
    elif isinstance(value, float):
        return value_html.format(value=f"{value:.2%}")


def _format_color_spaces(color: BaseColor, color_types):
    spaces = ""
    for color_type in color_types:
        spaces += SPACE_HTML.format(name=color_type, values=_value_formatter(color.to_color_type(color_type)))

    return spaces


def _format_map_spaces(map):
    spaces = ""
    for key, color in map.items():
        spaces += MAP_COLOR_HTML.format(color=color.hex, text=f"{key}: {color.hex}")

    return spaces


def _format_palette_spaces(palette):
    spaces = ""
    for color in palette:
        spaces += MAP_COLOR_HTML.format(color=color.hex, text=f"{color.hex}")

    return spaces


def _calc_grad(scale):
    grad = ", ".join([f"{color.hex} {stop:.0%}" for color, stop in zip(scale, scale.stops)])

    return grad


def _format_scale_spaces(scale):
    spaces = ""
    for color, stop in zip(scale, scale.stops):
        spaces += SPACE_HTML.format(
            name=color.name if color.name is not None else "",
            values=(
                # TODO: use default type?
                _value_formatter(f"{color.hex}")
                + "\n"
                + _value_formatter(f"{stop:.2%}")
            ),
        )

    return spaces


def create_colorcamp_report(
    camp: Camp,
    report_path: Optional[Union[Path, str]] = None,
    color_types: Optional[List[ColorSpace]] = None,
    sections: Optional[List[ColorObject]] = None,
):
    if report_path is None:
        report_path = Path(".") / f"{camp.name}.html"

    PathValidator().validate(report_path)

    css_path = Path(__file__).parent / "css" / "report.css"

    with open(css_path, "r") as file:
        css = file.read()

    if camp.description is None:
        description = ""
    else:
        description = camp.description

    if sections is None:
        sections = ("colors", "palettes", "scales", "maps")
    else:
        # TODO: validate sections
        pass

    if color_types is None:
        # TODO: make this dynamic
        color_types = ["Hex", "RGB", "HSL"]

    section_html = ""
    for section in sections:
        section_dict = getattr(camp, section).to_dict()

        if section == "colors":
            content = "".join(
                [
                    COLOR_HTML.format(
                        name=name,
                        color=color.hex,
                        spaces=_format_color_spaces(color, color_types),
                    )
                    for name, color in section_dict.items()
                ]
            )
        elif section == "palettes":
            content = "".join(
                [
                    MAP_HTML.format(name=name, colors=_format_palette_spaces(palette))
                    for name, palette in section_dict.items()
                ]
            )
        elif section == "scales":
            content = "".join(
                [
                    SCALE_HTML.format(
                        name=name,
                        grad=_calc_grad(scale),
                        spaces=_format_scale_spaces(scale),
                    )
                    for name, scale in section_dict.items()
                ]
            )
        elif section == "maps":
            content = "".join(
                [MAP_HTML.format(name=name, colors=_format_map_spaces(map)) for name, map in section_dict.items()]
            )
        else:
            content = ""

        section_html += SECTION_HTML.format(section_name=section.title(), content=content)

    report = REPORT_TEMPLATE.format(
        css=css,
        camp_name=camp.name,
        description=description,
        sections_html=section_html,
    )

    with open(report_path, "w") as file:
        file.write(report)
