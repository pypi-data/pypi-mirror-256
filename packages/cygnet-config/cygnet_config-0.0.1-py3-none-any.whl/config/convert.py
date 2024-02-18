import inspect
import typing as t
from pathlib import Path

from cattrs import Converter as CattrsConverter

from . import registry
from .utils import dispatch, exists_in_path, load


class Converter(CattrsConverter):
    def __init__(
        self,
        *args,
        registry=registry,
        type_field: str = "__type__",
        add_protocol_hook=True,
        add_class_hook=True,
        add_callable_hook=True,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.registry = registry
        self.type_field = type_field
        if add_protocol_hook:
            self.register_deprioritized_structure_hook_func(
                lambda cl: getattr(cl, "_is_protocol", False), self.structure_protocol
            )
        if add_callable_hook:
            self.register_deprioritized_structure_hook_func(
                lambda cl: getattr(cl, "__name__", None) == "Callable",
                self.structure_callable,
            )
        if add_class_hook:
            self.register_deprioritized_structure_hook_func(
                lambda _: True, self.structure_annotated_class
            )

    def register_deprioritized_structure_hook_func(self, predicate, handler):
        self._structure_func._function_dispatch._handler_pairs.insert(
            -1, (predicate, handler, False)
        )
        self._structure_func.clear_direct()
        self._structure_func.dispatch.cache_clear()

    def structure_annotated_class(self, fields, cl):
        if (
            isinstance(fields, str)
            and exists_in_path(Path(fields))
            and not issubclass(cl, (str, Path))
        ):
            fields = load(fields)
        signature = _parse_signature(cl)
        annotated_types = _parse_annotated_types_from_signature(signature)
        has_kwargs, kwarg_type = _parse_kwargs_from_signature(signature)
        validated = {}
        if not isinstance(fields, dict):
            if cl == t.Any:
                return fields
            return cl(fields)
        for key, field in fields.items():
            if key not in signature:
                if has_kwargs:
                    validated[key] = self.structure(field, kwarg_type)
                continue
            if annotated_types[key] == t.Any:
                validated[key] = field
            else:
                validated[key] = self.structure(field, annotated_types[key])
        return cl(**validated)

    def structure_protocol(self, fields, cl):
        return self.structure_ambiguous_type(
            fields=fields, cl=cl, validate=self._validate_protocol_or_raise
        )

    def structure_callable(self, fields, cl):
        return self.structure_ambiguous_type(
            fields=fields, cl=cl, validate=self._validate_callable_or_raise
        )

    def structure_ambiguous_type(self, *, fields, cl, validate: t.Callable):
        if isinstance(fields, str):
            built = self._structure_protocol_from_str(fields, cl)
        else:
            if self.type_field not in fields:
                raise ValueError(
                    "Structuring ambiguous type {cl} requires a "
                    f"'{self.type_field}' field in dict {fields}"
                )
            source = fields.pop(self.type_field)
            if isinstance(source, str):
                source = self._try_import_or_dispatch(source)
            built = self.structure(fields, source)
        validate(built, cl)
        return built

    def _validate_protocol_or_raise(self, built, cl):
        try:
            valid = isinstance(built, cl)
        except TypeError:
            # protocol check is not enabled unless protocol has @runtime_checkable decorator
            valid = True
        if not valid:
            raise (ValueError(f"{type(built)} is not a valid instance of {cl}"))

    def _validate_callable_or_raise(self, built, callable_type):
        valid = callable(built)
        if not valid:
            name = getattr(built, "__name__", str(built))
            raise (ValueError(f"{name} is not a valid instance of {callable_type}"))

    def _structure_protocol_from_str(self, fields: str, cl):
        try:
            return self._try_import_or_dispatch(fields)
        except ModuleNotFoundError:
            pass  # was not able to dispatch
        if not exists_in_path(Path(fields)):
            raise ValueError(
                f"{fields} cannot be resolved to a valid python "
                "object or path to config file"
            )
        fields = load(fields)
        return self.structure_protocol(fields, cl)

    def _try_import_or_dispatch(self, source: str):
        if source in self.registry:
            return self.registry[source]
        return dispatch(source)


def _parse_kwargs_from_signature(
    class_params: t.Mapping[str, inspect.Parameter],
) -> t.Tuple[t.Optional[str], t.Any]:
    """Parse the type annotation of **kwargs parameter from the parameter signature.

    :param class_params: Mapping of class/function signature parameters.

    :returns:
        kwarg_name: If not None, then the name assigned to the dictionary of keyword
            arguments that aren't bound to any other parameter in a class/function
            signature. This is typically the name "kwargs".
        kwarg_type: The type corresponding to "kwargs".
    """

    kwarg_name = None
    kwarg_type = t.Any
    for param_name, param in class_params.items():
        if param.kind == param.VAR_KEYWORD:
            kwarg_name = param_name
            kwarg_type = (
                param.annotation if (param.annotation != param.empty) else t.Any
            )
            break
    return kwarg_name, kwarg_type


def _parse_annotated_types_from_signature(signature: t.Mapping[str, inspect.Parameter]):
    annotated_types = {}
    for key, param in signature.items():
        if param.annotation == inspect.Parameter.empty:
            annotated_types[key] = t.Any
        else:
            annotated_types[key] = param.annotation
    return annotated_types


def _parse_signature(
    source: t.Union[t.Callable, t.Type],
) -> t.Mapping[str, inspect.Parameter]:
    """Return the signature of source.

    :param source: Either a class or function type.

    :return: Mapping of class/function signature parameters to inspect.Parameters.
        If source is a class, then the parameter signature of the __init__ method
        is returned.

    :raises ValueError: If source is neither a class nor a function type.
    """

    if inspect.isclass(source):
        return inspect.signature(source.__init__).parameters  # type: ignore
    try:
        return inspect.signature(source).parameters
    except TypeError as e:
        raise TypeError(f"Cannot parse signature of {source}") from e
