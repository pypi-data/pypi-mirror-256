import typing as t

from config import registry
from config.convert import Converter
from config.helpers import partial


def mock_func(x: int, y: int, z: int):
    return x + 10 * y + 100 * z


class TestHelpers:
    def test_partial_is_registered(self):
        reg = registry["partial"]
        assert reg == partial

    def test_partial_is_structurable(self):
        c = Converter()
        source = {
            "__type__": "partial",
            "function": "tests.integration.test_helpers.mock_func",
            "args": [1],
            "z": 5,
        }
        result = c.structure(source, t.Callable)
        assert result(3) == 531
