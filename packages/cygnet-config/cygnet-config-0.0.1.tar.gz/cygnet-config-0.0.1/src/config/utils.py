import importlib
import json
import logging
import os
import pickle
import random
import typing as t
from pathlib import Path

logger = logging.getLogger(__name__)


def exists_in_path(filepath: Path) -> bool:
    if filepath.exists():
        return True
    configpath = os.environ.get("CONFIGPATH", "")
    paths = [Path(p) for p in configpath.split(":")]
    for path in paths:
        if (path / filepath).exists():
            return True
    return False


def find_in_path(filepath: Path) -> Path:
    if filepath.exists():
        return filepath
    configpath = os.environ.get("CONFIGPATH", "")
    paths = [Path(p) for p in configpath.split(":")]
    for path in paths:
        if (path / filepath).exists():
            return path / filepath
    raise FileNotFoundError(f"{filepath} not found. Current CONFIGPATH: {configpath}")


def parse_attribute_string(classpath: str) -> t.Tuple[str, str]:
    pieces = classpath.split(".")
    modulepath = ".".join(pieces[:-1])
    classname = pieces[-1]
    return modulepath, classname


def dispatch(attributepath: str, default_module: t.Optional[str] = None) -> t.Any:
    module, attribute = parse_attribute_string(attributepath)
    module = module or default_module
    if not module:
        raise (
            ValueError(
                f"Cannot find base module to import in provided string {attributepath}"
            )
        )
    module = importlib.import_module(module)
    if hasattr(module, attribute):
        return getattr(module, attribute)
    raise ValueError("{} not found in {}".format(attribute, module))


def load(filepath: t.Union[str, Path]) -> t.Any:
    filepath = Path(filepath)
    filepath = find_in_path(filepath)
    kwargs = {}
    if filepath.suffix.lower() in [".yaml", ".yml"]:
        import yaml

        module = yaml
        kwargs["Loader"] = yaml.FullLoader
        filetype = "r"
    elif filepath.suffix.lower() in [".pkl", ".pickle"]:
        module = pickle
        filetype = "rb"
    elif filepath.suffix.lower() == ".json":
        module = json
        filetype = "r"
    elif filepath.suffix.lower() in [".tml", ".toml"]:
        assert False, "toml not yet implemented"
    else:
        raise ValueError(
            "Extension {} not supported. Use yaml, pkl, json, or toml".format(
                filepath.suffix
            )
        )
    with filepath.open(filetype) as f:
        data = module.load(f, **kwargs)
    return data


def save(data: t.Dict, filepath: t.Union[str, Path], safe: bool = False, **kwargs):
    filepath = Path(filepath)
    filepath.parent.mkdir(exist_ok=True, parents=True)
    tmpfile = filepath.with_suffix(".{}.tmp".format(random.randint(0, 20000)))
    if filepath.suffix.lower() in [".yaml", ".yml"]:
        import yaml

        module = yaml
        defaults: t.Dict[str, t.Any] = {"default_flow_style": False, "sort_keys": False}
        filetype = "w"
    elif filepath.suffix.lower() in [".pkl", ".pickle"]:
        module = pickle
        defaults = {}
        filetype = "wb"
    else:
        module = json
        defaults = {"sort_keys": True, "indent": 4}
        filetype = "w"
    defaults.update(kwargs)
    if safe:
        with tmpfile.open(filetype) as f:
            module.dump(data, f, **defaults)
        tmpfile.rename(filepath)
    else:
        with filepath.open(filetype) as f:
            module.dump(data, f, **defaults)


def coerce_str_to_path(path: t.Optional[t.Union[str, Path]]) -> t.Optional[Path]:
    if not path:
        return None
    return Path(path)


def prepend_keys(x: t.Dict[str, t.Any], prefix: str) -> t.Dict[str, t.Any]:
    return {prefix + key: value for key, value in x.items()}


def recursive_update(
    original: t.Dict[str, t.Any],
    new: t.Dict[str, t.Any],
) -> t.Dict[str, t.Any]:
    """Recursively update (key, value) pairs in the original dictionary using the new
    dictionary.

    :param original: Original dictionary to update (key, value) pairs for.
    :param new: Dictionary containing potentially new (key, value) pairs to update in
        original.

    :return: The updated dictionary.

    :raises ValueError: If new is not a dictionary.
    """

    if not isinstance(original, dict):
        return new
    if not isinstance(new, dict):
        raise ValueError(f"Cannot update dict {original} with non-dict {new}")
    result = {}
    for key, value in original.items():
        if key in new:
            result[key] = _recursive_update(value, new[key])
        else:
            result[key] = value
    for key, value in new.items():
        if key in original:
            continue
        result[key] = value
    return result


def _recursive_update(
    original: t.Dict[str, t.Any],
    new: t.Union[str, t.Dict[str, t.Any]],
) -> t.Union[str, t.Dict[str, t.Any]]:
    if not isinstance(original, dict):
        return new
    if not isinstance(new, dict):
        raise ValueError(f"Cannot update dict {original} with non-dict {new}")
    result = {}
    for key, value in original.items():
        if key in new:
            result[key] = _recursive_update(value, new[key])
        else:
            result[key] = value
    for key, value in new.items():
        if key in original:
            continue
        result[key] = value
    return result


def parse_key_value_pair(key_value_pair: str) -> t.Dict[str, t.Any]:
    """Return a dictionary whose (key, value) pairs are constructed from args.

    :param key_value_pair: String of the form: "a[.b[...]]=d".

    :return: Nested dictionary where "." indicates nesting and "=" indicates
    the final value. Any "-" in the key is converted to "_".

    Examples:

    >>> _parse_key_value_pair("a=b")
    {"a": "b"}

    >>> _parse_key_value_pair("a.b=c")
    {"a": {"b": "c"}}

    >>> _parse_key_value_pair("a.b.c=d")
    {"a": {"b": {"c": "d"}}}
    """

    key, value = key_value_pair.split("=")
    keys = list(_remap_dashes(key).split("."))
    return _populate_nested_dict(*keys, value)  # type: ignore


def _populate_nested_dict(
    key: str, *nested_keys: str
) -> t.Union[str, t.Dict[str, t.Any]]:
    if not nested_keys:
        return key
    return {
        key: _populate_nested_dict(  # pylint: disable=no-value-for-parameter
            *nested_keys
        )
    }


def _remap_dashes(x: str) -> str:
    """Remap "-" to "_" in x.

    :param x: String to remap.

    :return: Remapped string with "-" converted to "_".
    """

    return "_".join(x.split("-"))
