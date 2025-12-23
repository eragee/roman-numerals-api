import re

_ROMAN_ALLOWED = re.compile(r"^[IVXLCDM]+$", re.IGNORECASE)
_INT_ALLOWED = re.compile(r"^[0-9]+$")

_ROMAN_VALUES = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}

_INT_TO_ROMAN_TABLE = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)


def is_valid_roman_charset(value: str) -> bool:
    return bool(value) and bool(_ROMAN_ALLOWED.fullmatch(value))


def is_valid_int_charset(value: str) -> bool:
    return bool(value) and bool(_INT_ALLOWED.fullmatch(value))


def int_to_roman(value: int) -> str:
    if value < 1 or value > 3999:
        raise ValueError("Integer out of supported range (1..3999).")

    n = value
    out = []
    for base, sym in _INT_TO_ROMAN_TABLE:
        if n <= 0:
            break
        count = n // base
        if count:
            out.append(sym * count)
            n -= base * count
    return "".join(out)


def _roman_to_int_loose(roman: str) -> int:
    r = roman.upper()
    total = 0
    i = 0
    while i < len(r):
        cur = _ROMAN_VALUES.get(r[i])
        if cur is None:
            raise ValueError("Invalid Roman character encountered.")

        if i + 1 < len(r):
            nxt = _ROMAN_VALUES.get(r[i + 1])
            if nxt is None:
                raise ValueError("Invalid Roman character encountered.")
            if cur < nxt:
                total += (nxt - cur)
                i += 2
                continue

        total += cur
        i += 1

    return total


def roman_to_int_strict(roman: str) -> int:
    if not is_valid_roman_charset(roman):
        raise ValueError("Roman numeral contains invalid characters; allowed: IVXLCDM (case-insensitive).")

    normalized = roman.upper()
    value = _roman_to_int_loose(normalized)

    if value < 1 or value > 3999:
        raise ValueError("Roman numeral out of supported range (1..3999).")

    canonical = int_to_roman(value)
    if canonical != normalized:
        raise ValueError("Roman numeral is not canonical (permissive forms like IIII are rejected).")

    return value
