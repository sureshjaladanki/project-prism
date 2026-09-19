"""Tiny Census-shaped PCA / A-02 workbooks for ingest tests. Not producer bytes."""

from __future__ import annotations

from io import BytesIO

import xlwt  # type: ignore[import-untyped]
from openpyxl import Workbook

from prism.ingest.parse_c2 import PCA_COLUMNS


def pca_workbook_bytes() -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    assert sheet is not None
    sheet.title = "Sheet1"
    sheet.append(list(PCA_COLUMNS))
    sheet.append(["00", "000", "India", "India", "Total", 10, 100, 55, 45])
    sheet.append(["00", "000", "India", "India", "Rural", 6, 60, 32, 28])
    sheet.append(["00", "000", "India", "India", "Urban", 4, 40, 23, 17])
    sheet.append(["28", "000", "STATE", "ANDHRA PRADESH", "Total", 3, 30, 16, 14])
    sheet.append(["99", "001", "DISTRICT", "SHOULD NOT APPEAR", "Total", 1, 1, 1, 0])
    workbook.create_sheet("Sheet2")
    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()


def scanned_projection_pdf_bytes() -> bytes:
    return b"%PDF-1.5\n1 0 obj<</Type/XObject/Subtype/Image>>endobj\n%%EOF"


def ole_xls_bytes() -> bytes:
    return b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1" + b"\x00" * 32


def _pdf_stream(items: list[tuple[str, float, float]], height: float) -> str:
    ops = ["BT", "/F1 9 Tf"]
    for text, x, top in items:
        escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        ops.append(f"1 0 0 1 {x:.2f} {height - top:.2f} Tm ({escaped}) Tj")
    ops.append("ET")
    return "\n".join(ops)


def positioned_pdf_bytes(
    pages: list[list[tuple[str, float, float]]],
    *,
    width: float = 612,
    height: float = 792,
) -> bytes:
    kids = " ".join(f"{3 + index} 0 R" for index in range(len(pages)))
    objects = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>",
    ]
    content_ids = [3 + len(pages) + index for index in range(len(pages))]
    font_id = 3 + 2 * len(pages)
    streams = [_pdf_stream(items, height) for items in pages]
    for index in range(len(pages)):
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width:.2f} {height:.2f}] "
            f"/Contents {content_ids[index]} 0 R "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> >>"
        )
    for stream in streams:
        objects.append(
            f"<< /Length {len(stream.encode('latin-1'))} >>\nstream\n{stream}\nendstream"
        )
    objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    chunks = [b"%PDF-1.4\n"]
    offsets = [0]
    cursor = 9
    for index, obj in enumerate(objects, start=1):
        chunk = f"{index} 0 obj\n{obj}\nendobj\n".encode("latin-1")
        offsets.append(cursor)
        chunks.append(chunk)
        cursor += len(chunk)
    xref_lines = [f"xref\n0 {len(objects) + 1}\n", "0000000000 65535 f \n"]
    xref_lines.extend(f"{offset:010d} 00000 n \n" for offset in offsets[1:])
    trailer = (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{cursor}\n%%EOF\n"
    ).encode("latin-1")
    return b"".join(chunks) + "".join(xref_lines).encode("latin-1") + trailer


def bulletin_table1_pdf_bytes() -> bytes:
    residences = ("Total", "Rural", "Urban") * 4
    xs = [200 + 32 * index for index in range(12)]
    header = [(token, float(x), 80.0) for token, x in zip(residences, xs, strict=True)]
    numbers = [(str(index + 1), float(x), 90.0) for index, x in enumerate([40, *xs])]
    india = [("India", 20.0, 120.0)] + [
        (value, float(x), 120.0)
        for value, x in zip(
            (
                "18.3",
                "20.2",
                "14.7",
                "6.4",
                "6.8",
                "5.6",
                "11.9",
                "13.5",
                "9.0",
                "24",
                "27",
                "17",
            ),
            xs,
            strict=True,
        )
    ]
    dnh = [
        ("3.", 20.0, 160.0),
        ("Dadra", 38.0, 160.0),
        ("&", 72.0, 160.0),
        ("Nagar", 84.0, 160.0),
        ("Haveli", 120.0, 160.0),
    ] + [("1.0", float(x), 160.0) for x in xs]
    wrap = [
        ("and", 20.0, 168.0),
        ("Daman", 40.0, 168.0),
        ("&", 78.0, 168.0),
        ("Diu", 90.0, 168.0),
    ]
    note = [("Note:", 20.0, 400.0)]
    footer = [("4", 300.0, 500.0)]
    title = [
        ("Table", 40.0, 40.0),
        ("1:", 70.0, 40.0),
        ("Estimated", 90.0, 40.0),
        ("Birth", 140.0, 40.0),
        ("Rate", 170.0, 40.0),
    ]
    return positioned_pdf_bytes(
        [title + header + numbers + india + dnh + wrap + note + footer]
    )


def table3_fertility_pdf_bytes() -> bytes:
    xs = (220.0, 280.0, 340.0)
    title = [
        ("Table", 40.0, 40.0),
        ("3", 70.0, 40.0),
        ("Fertility", 100.0, 40.0),
        ("Indicators,", 150.0, 40.0),
        ("2024", 230.0, 40.0),
    ]
    header = [
        ("Total", xs[0], 80.0),
        ("Rural", xs[1], 80.0),
        ("Urban", xs[2], 80.0),
    ]
    india = [("India", 40.0, 110.0)]
    tfr = [
        ("Total", 40.0, 140.0),
        ("Fertility", 70.0, 140.0),
        ("Rate", 120.0, 140.0),
        ("1.9", xs[0], 140.0),
        ("2.1", xs[1], 140.0),
        ("1.5", xs[2], 140.0),
    ]
    return positioned_pdf_bytes([title + header + india + tfr])


def table8_projection_pdf_bytes() -> bytes:
    xs = (120.0, 170.0, 220.0, 280.0, 330.0, 380.0, 440.0, 490.0, 540.0)
    title = [
        ("TABLE", 40.0, 40.0),
        ("-", 90.0, 40.0),
        ("8", 100.0, 40.0),
        ("Projected", 120.0, 40.0),
        ("Total", 180.0, 40.0),
        ("Population", 220.0, 40.0),
    ]
    names = [
        ("INDIA", 150.0, 70.0),
        ("PUNJAB", 310.0, 70.0),
        ("GOA", 470.0, 70.0),
    ]
    year_header = [("Year", 40.0, 90.0)]
    header = [
        (token, x, 110.0)
        for token, x in zip(
            ("Persons", "Male", "Females") * 3, xs, strict=True
        )
    ]
    row_2011 = [("2011", 40.0, 140.0)] + [
        (value, x, 140.0)
        for value, x in zip(
            ("12,10,855", "623", "587", "2,774", "1,464", "1,310", "146", "74", "72"),
            xs,
            strict=True,
        )
    ]
    row_2036 = [("2036", 40.0, 160.0)] + [
        (value, x, 160.0)
        for value, x in zip(
            ("15,00,000", "700", "650", "3,000", "1,500", "1,400", "160", "80", "80"),
            xs,
            strict=True,
        )
    ]
    footer = [("47", 300.0, 500.0)]
    return positioned_pdf_bytes(
        [title + names + year_header + header + row_2011 + row_2036 + footer]
    )


def a02_workbook_bytes() -> bytes:
    book = xlwt.Workbook()
    sheet = book.add_sheet("A-2")
    sheet.write_merge(0, 0, 0, 8, "A - 2  DECADAL VARIATION  IN  POPULATION  SINCE  1901")
    sheet.write(1, 0, "State")
    sheet.write(1, 1, "District")
    sheet.write(1, 2, "India/State/")
    sheet.write(1, 3, "Census")
    sheet.write(1, 4, "Persons")
    sheet.write_merge(1, 1, 5, 6, "Variation since the")
    sheet.write(1, 7, "Males")
    sheet.write(1, 8, "Females")
    sheet.write(2, 0, "Code")
    sheet.write(2, 1, "Code")
    sheet.write(2, 2, "Union Territory")
    sheet.write(2, 3, "Year")
    sheet.write_merge(2, 2, 5, 6, "preceding census")
    sheet.write(3, 5, "Absolute")
    sheet.write(3, 6, "Percentage")
    for index in range(9):
        sheet.write(4, index, index + 1)
    sheet.write(6, 0, "00")
    sheet.write(6, 1, "000")
    sheet.write(6, 2, "INDIA")
    sheet.write(6, 3, "  1901 $")
    sheet.write(6, 4, 238396327)
    sheet.write(6, 5, "                ---")
    sheet.write(6, 6, "              ---")
    sheet.write(6, 7, 120791301)
    sheet.write(6, 8, 117358672)
    sheet.write(7, 3, 2011)
    sheet.write(7, 4, 1210854977)
    sheet.write(7, 5, 182117541)
    sheet.write(7, 6, 17.7)
    sheet.write(7, 7, 623270258)
    sheet.write(7, 8, 587584719)
    sheet.write(8, 0, "12")
    sheet.write(8, 1, "000")
    sheet.write(8, 2, "Arunachal Pradesh *")
    sheet.write(8, 3, 1901)
    sheet.write(8, 4, "N.A")
    sheet.write(8, 5, "-")
    sheet.write(8, 6, "-")
    sheet.write(8, 7, "N.A.")
    sheet.write(8, 8, "N.A.")
    sheet.write(9, 0, "25")
    sheet.write(9, 1, "000")
    sheet.write(9, 2, "Daman & Diu ")
    sheet.write(9, 3, 1900)
    sheet.write(9, 4, 32005)
    sheet.write(9, 5, "                   ---")
    sheet.write(9, 6, "               ---")
    sheet.write(9, 7, 16046)
    sheet.write(9, 8, 15959)
    sheet.write(10, 0, "99")
    sheet.write(10, 1, "001")
    sheet.write(10, 2, "SHOULD NOT APPEAR")
    sheet.write(10, 3, 2011)
    sheet.write(10, 4, 1)
    sheet.write(10, 5, "---")
    sheet.write(10, 6, "---")
    sheet.write(10, 7, 1)
    sheet.write(10, 8, 0)
    sheet.write(11, 3, 2001)
    sheet.write(11, 4, 2)
    sheet.write(12, 2, "    N.A.: -    Not available.")
    buffer = BytesIO()
    book.save(buffer)
    return buffer.getvalue()
