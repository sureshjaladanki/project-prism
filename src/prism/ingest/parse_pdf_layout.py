"""PDF word-to-column assignment. Stop if a token does not map uniquely."""

from __future__ import annotations

import re
from dataclasses import dataclass

_AMOUNT = re.compile(r"^[*(—–-]*\d[\d,.]*$")
_WITHHELD = frozenset({"…", "...", "..", ".", "-", "–", "—"})


@dataclass(frozen=True)
class PdfWord:
    text: str
    x0: float
    x1: float
    top: float

    @property
    def xmid(self) -> float:
        return (self.x0 + self.x1) / 2


@dataclass(frozen=True)
class PdfColumn:
    name: str
    token: str


@dataclass(frozen=True)
class AssignedTable:
    rows: list[dict[str, str]]
    assigned: int
    ambiguous: int
    centers: tuple[float, ...]
    header_index: int
    left: float
    half: float


def is_amount_token(text: str) -> bool:
    stripped = text.replace(",", "").strip()
    if stripped in _WITHHELD:
        return True
    return bool(_AMOUNT.fullmatch(stripped))


def cluster_rows(words: list[PdfWord], y_tol: float = 3.0) -> list[list[PdfWord]]:
    ordered = sorted(words, key=lambda word: (word.top, word.x0))
    buckets: list[list[PdfWord]] = []
    for word in ordered:
        if buckets and abs(word.top - buckets[-1][0].top) <= y_tol:
            buckets[-1].append(word)
        else:
            buckets.append([word])
    return buckets


def nearest_column(xmid: float, centers: tuple[float, ...], half: float) -> int | None:
    dists = sorted((abs(xmid - center), i) for i, center in enumerate(centers))
    nearest = dists[0][0]
    if nearest > half:
        return None
    if len(dists) > 1 and abs(dists[0][0] - dists[1][0]) < 0.5:
        return None
    return dists[0][1]


def page_words(page: object) -> list[PdfWord]:
    extract_words = page.extract_words  # type: ignore[attr-defined]
    words: list[PdfWord] = []
    for raw in extract_words() or []:
        words.append(
            PdfWord(
                text=str(raw["text"]),
                x0=float(raw["x0"]),
                x1=float(raw["x1"]),
                top=float(raw["top"]),
            )
        )
    return words


def words_before(words: list[PdfWord], prefix: str) -> list[PdfWord]:
    hits = [word for word in words if word.text.startswith(prefix)]
    if not hits:
        return words
    cut = min(word.top for word in hits)
    return [word for word in words if word.top < cut]


def words_through(words: list[PdfWord], token: str, pad: float = 10.0) -> list[PdfWord]:
    hits = [word for word in words if word.text == token]
    if not hits:
        return words
    cut = max(word.top for word in hits) + pad
    return [word for word in words if word.top <= cut]


def group_centers(centers: tuple[float, ...], width: int = 3) -> tuple[float, ...]:
    return tuple(
        sum(centers[index : index + width]) / width
        for index in range(0, len(centers), width)
    )


def names_from_groups(
    words: list[PdfWord],
    centers: tuple[float, ...],
    half: float,
    *,
    left: float,
) -> list[str] | None:
    buckets: list[list[str]] = [[] for _ in centers]
    for word in sorted(words, key=lambda item: (item.x0, item.top)):
        if word.xmid < left:
            continue
        if is_amount_token(word.text):
            continue
        index = nearest_column(word.xmid, centers, half)
        if index is None:
            return None
        buckets[index].append(word.text)
    names = [" ".join(parts) for parts in buckets]
    if any(not name for name in names):
        return None
    return names


def _consume_header(
    row: list[PdfWord], tokens: tuple[str, ...]
) -> list[PdfWord] | None:
    remaining = list(tokens)
    used: list[PdfWord] = []
    for word in sorted(row, key=lambda item: item.x0):
        if remaining and word.text == remaining[0]:
            used.append(word)
            remaining.pop(0)
    if remaining:
        return None
    return used


def assign_pdf_table(
    words: list[PdfWord],
    columns: tuple[PdfColumn, ...],
    *,
    y_tol: float = 3.0,
) -> AssignedTable | None:
    tokens = tuple(column.token for column in columns)
    names = tuple(column.name for column in columns)
    buckets = cluster_rows(words, y_tol)
    header_words: list[PdfWord] | None = None
    header_index: int | None = None
    for index, bucket in enumerate(buckets):
        found = _consume_header(bucket, tokens)
        if found is None:
            continue
        header_words = found
        header_index = index
        break
    if header_words is None or header_index is None:
        return None
    centers = tuple((word.x0 + word.x1) / 2 for word in header_words)
    left = min(word.x0 for word in header_words) - 8
    gaps = [centers[i + 1] - centers[i] for i in range(len(centers) - 1)]
    half = min(gaps) / 2
    assigned = 0
    ambiguous = 0
    rows: list[dict[str, str]] = []
    for bucket in buckets[header_index + 1 :]:
        record = {name: "" for name in names}
        labels: list[str] = []
        for word in bucket:
            if word.xmid < left:
                labels.append(word.text)
                continue
            if not is_amount_token(word.text):
                labels.append(word.text)
                continue
            if word.text.strip() in _WITHHELD:
                dists = sorted(
                    (abs(word.xmid - center), i) for i, center in enumerate(centers)
                )
                if dists[0][0] > half:
                    ambiguous += 1
                    continue
                assigned += 1
                continue
            column = nearest_column(word.xmid, centers, half)
            if column is None:
                ambiguous += 1
                continue
            assigned += 1
            record[names[column]] = word.text.lstrip("*")
        if not labels and not any(record.values()):
            continue
        record["line_label"] = " ".join(labels)
        rows.append(record)
    return AssignedTable(
        rows=rows,
        assigned=assigned,
        ambiguous=ambiguous,
        centers=centers,
        header_index=header_index,
        left=left,
        half=half,
    )
