"""Static gates on generated Vega-Lite JSON (blueprint test 8)."""

from __future__ import annotations

from typing import Any

MEASURE_FIELDS = frozenset({"plotValue", "value", "inflation"})
STATE_AXIS_FIELDS = frozenset({"geography_name_en", "geography_code"})
RED_GREEN_SCHEMES = frozenset(
    {
        "redgreen",
        "redyellowgreen",
        "greenyellowred",
        "redbluegreen",
    }
)


class ChartSpecError(ValueError):
    pass


def assert_chart_rows_cited(rows: list[dict[str, object]]) -> None:
    for row in rows:
        if row.get("value") is None:
            continue
        citation = row.get("citation")
        if not isinstance(citation, dict) or not citation.get("citation_id"):
            raise ChartSpecError("chart payload cannot include a number without its citation card")
        if not citation.get("producer") or not citation.get("series"):
            raise ChartSpecError("citation card is missing producer or series")


def assert_state_axis_not_ranked(spec: dict[str, Any]) -> None:
    for encoding in _encodings(spec):
        for channel, axis in encoding.items():
            if channel not in {"x", "y"} or not isinstance(axis, dict):
                continue
            if axis.get("field") not in STATE_AXIS_FIELDS:
                continue
            sort = axis.get("sort")
            if _sort_is_measure(sort, encoding, channel):
                raise ChartSpecError("state/UT axis must not be sorted by a measure")


def assert_no_red_green_diverging(spec: dict[str, Any]) -> None:
    for encoding in _encodings(spec):
        color = encoding.get("color")
        if not isinstance(color, dict):
            continue
        scale = color.get("scale")
        if not isinstance(scale, dict):
            continue
        scheme = scale.get("scheme")
        if isinstance(scheme, str) and _scheme_is_red_green(scheme):
            raise ChartSpecError("colour scale must not be red–green diverging")
        if isinstance(scheme, dict):
            name = scheme.get("name")
            if isinstance(name, str) and _scheme_is_red_green(name):
                raise ChartSpecError("colour scale must not be red–green diverging")
        color_range = scale.get("range")
        if isinstance(color_range, list) and _range_is_red_green(color_range):
            raise ChartSpecError("colour scale must not be red–green diverging")


def assert_generated_spec(spec: dict[str, Any]) -> None:
    assert_state_axis_not_ranked(spec)
    assert_no_red_green_diverging(spec)
    for rows in _data_values(spec):
        assert_chart_rows_cited(rows)


def _encodings(node: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, dict):
        encoding = node.get("encoding")
        if isinstance(encoding, dict):
            found.append(encoding)
        for value in node.values():
            found.extend(_encodings(value))
    elif isinstance(node, list):
        for item in node:
            found.extend(_encodings(item))
    return found


def _data_values(node: Any) -> list[list[dict[str, object]]]:
    found: list[list[dict[str, object]]] = []
    if isinstance(node, dict):
        data = node.get("data")
        if isinstance(data, dict) and isinstance(data.get("values"), list):
            rows = data["values"]
            if rows and isinstance(rows[0], dict) and "observation_id" in rows[0]:
                found.append(rows)
        for value in node.values():
            found.extend(_data_values(value))
    elif isinstance(node, list):
        for item in node:
            found.extend(_data_values(item))
    return found


def _sort_is_measure(sort: Any, encoding: dict[str, Any], channel: str) -> bool:
    if sort is None:
        return False
    if isinstance(sort, str) and sort in {"x", "y", "-x", "-y"}:
        other = "x" if channel == "y" else "y"
        other_enc = encoding.get(other)
        if isinstance(other_enc, dict) and other_enc.get("field") in MEASURE_FIELDS:
            return True
        return sort.lstrip("-") != channel
    if isinstance(sort, dict):
        field = sort.get("field")
        if field in MEASURE_FIELDS:
            return True
        if sort.get("op") is not None and field in MEASURE_FIELDS:
            return True
    return False


def _scheme_is_red_green(name: str) -> bool:
    compact = name.lower().replace("-", "").replace("_", "")
    if compact in RED_GREEN_SCHEMES:
        return True
    return "red" in compact and "green" in compact


def _range_is_red_green(color_range: list[Any]) -> bool:
    texts = [item.lower() for item in color_range if isinstance(item, str)]
    has_red = any("red" in item or item.startswith("#d62") or item in {"#f00", "#ff0000"} for item in texts)
    has_green = any(
        "green" in item or item.startswith("#2ca") or item in {"#0f0", "#00ff00"} for item in texts
    )
    return has_red and has_green
