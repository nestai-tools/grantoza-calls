"""Verify local originals or explicit references in a public package without originals."""
import hashlib
from pathlib import Path, PurePosixPath
import re


def source_matches(call, document, expected):
    call = Path(call).resolve()
    relative = document.get('plik', '')
    path = call / relative
    if (not relative or not path.resolve().is_relative_to(call)
            or not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected)
            or document.get('sha256') != expected):
        return False
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest() == expected
    # The hash identifies the upstream original; it does not verify an absent file.
    return (document.get('oryginal_w_pakiecie') is False
            and PurePosixPath(relative).parts[:2] == ('01-sources', 'originals'))
