"""Test fixtures."""

import pytest
from zero import Circuit
from .data import ZeroDataGenerator


@pytest.fixture
def circuit():
    return Circuit()


@pytest.fixture
def datagen():
    return ZeroDataGenerator()
