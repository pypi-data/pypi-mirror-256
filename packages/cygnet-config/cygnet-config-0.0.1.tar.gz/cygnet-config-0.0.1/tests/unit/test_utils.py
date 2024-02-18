import os

import pytest
from config.convert import Converter
from config.utils import (
    dispatch,
    load,
    parse_attribute_string,
    recursive_update,
    save,
)


class Test_recursive_update:
    def test_unested_dicts_update(self):
        original = {"foo": "old", "hello": "world"}
        result = recursive_update(original, {"foo": "bar", "buzz": "bazz"})
        assert result == {"foo": "bar", "hello": "world", "buzz": "bazz"}

    def test_updates_nested_dicts(self):
        original = {"foo": {"a": "old", "b": "b"}, "hello": "world"}
        result = recursive_update(original, {"foo": {"a": "new"}, "buzz": "bazz"})
        assert result == {
            "foo": {"a": "new", "b": "b"},
            "hello": "world",
            "buzz": "bazz",
        }

    def test_raises_if_nondict_used_to_update_dict(self):
        original = {"foo": {"a": "old", "b": "b"}, "hello": "world"}
        with pytest.raises(ValueError):
            recursive_update(original, {"foo": "not a dict"})

    def test_updates_doubly_nested_dicts(self):
        original = {"foo": {"a": {"c": "old", "d": "d"}, "b": "b"}, "hello": "world"}
        result = recursive_update(
            original, {"foo": {"a": {"c": "new"}}, "buzz": "bazz"}
        )
        assert result == {
            "foo": {"a": {"c": "new", "d": "d"}, "b": "b"},
            "hello": "world",
            "buzz": "bazz",
        }


def test_parse_class_string_splits_at_last_dot():
    result = parse_attribute_string("Class")
    assert result == ("", "Class")
    result = parse_attribute_string("module.Class")
    assert result == ("module", "Class")
    result = parse_attribute_string("pkg.mod1.Class")
    assert result == ("pkg.mod1", "Class")


def test_dispatch_uses_module_if_provided_in_classpath():
    result = dispatch("config.convert.Converter", "config.utils")
    assert result == Converter


def test_dispatch_uses_default_module_if_not_in_classpath():
    result = dispatch("Converter", "config.convert")
    assert result == Converter


class TestFileIO:
    def test_load_uses_CONFIGPATH_if_file_not_found(self, tmp_path):
        os.environ["CONFIGPATH"] = str(tmp_path)
        config = {"hello": "text string"}
        save(config, tmp_path / "foo.yaml")
        loaded = load("foo.yaml")
        assert config == loaded

    def test_load_ignores_CONFIGPATH_if_file_found(self, tmp_path):
        os.environ["CONFIGPATH"] = str(tmp_path)
        config = {"a": "foo"}
        (tmp_path / "tests/fixtures").mkdir(parents=True)
        save(config, tmp_path / "tests/fixtures/config.yaml")
        loaded = load("tests/fixtures/config.yaml")
        assert config != loaded
        assert loaded == {"foo": "hello", "bar": 123}

    def test_load_raises_if_file_not_in_path(self, tmp_path):
        config = {"hello": "text string"}
        save(config, tmp_path / "foo.yaml")
        with pytest.raises(FileNotFoundError):
            load("foo.yaml")
