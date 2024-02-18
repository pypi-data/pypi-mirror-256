"""Configuration component parser tests"""

import pytest
from zero.config import LibraryOpAmp


@pytest.mark.parametrize(
    "a0_abs,a0_db",
    (
        (1e6, "120 dB"),
        (1e6, "120dB"),
        (1e6, "120 db"),
        (1e6, "120db"),
        (1e6, "120 DB"),
        (1e6, "120DB"),
        (1e6, "120.0 dB"),
    )
)
def test_a0_db_scaling(a0_abs, a0_db):
    assert LibraryOpAmp(a0=a0_abs).a0 == LibraryOpAmp(a0=a0_db).a0
