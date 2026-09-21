"""HTML table expand with rowspan/colspan. Stop if the markup is not a grid."""

from __future__ import annotations

from html.parser import HTMLParser


class _HtmlTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[tuple[str, int, int]]]] = []
        self._table: list[list[tuple[str, int, int]]] | None = None
        self._row: list[tuple[str, int, int]] | None = None
        self._text: list[str] | None = None
        self._span: tuple[int, int] = (1, 1)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: (value or "") for key, value in attrs}
        if tag == "table":
            self._table = []
            self.tables.append(self._table)
        elif tag == "tr" and self._table is not None:
            self._row = []
            self._table.append(self._row)
        elif tag in {"td", "th"} and self._row is not None:
            self._text = []
            colspan = int(data["colspan"]) if data.get("colspan") else 1
            rowspan = int(data["rowspan"]) if data.get("rowspan") else 1
            self._span = (colspan, rowspan)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self._row is not None and self._text is not None:
            text = " ".join(" ".join(self._text).split())
            self._row.append((text, self._span[0], self._span[1]))
            self._text = None
        elif tag == "tr":
            self._row = None
        elif tag == "table":
            self._table = None

    def handle_data(self, data: str) -> None:
        if self._text is not None:
            self._text.append(data)


def parse_html_tables(html: str) -> list[list[list[tuple[str, int, int]]]]:
    parser = _HtmlTableParser()
    parser.feed(html)
    return parser.tables


def expand_html_table(rows: list[list[tuple[str, int, int]]]) -> list[list[str]]:
    occupied: dict[tuple[int, int], str] = {}
    for row_i, row in enumerate(rows):
        col = 0
        for text, colspan, rowspan in row:
            while (row_i, col) in occupied:
                col += 1
            for down in range(rowspan):
                for across in range(colspan):
                    key = (row_i + down, col + across)
                    if key not in occupied:
                        occupied[key] = text
            col += colspan
    if not occupied:
        return []
    max_r = max(row for row, _col in occupied)
    max_c = max(col for _row, col in occupied)
    return [
        [occupied.get((row, col), "") for col in range(max_c + 1)]
        for row in range(max_r + 1)
    ]
