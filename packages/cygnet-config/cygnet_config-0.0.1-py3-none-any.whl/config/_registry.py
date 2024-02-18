class Registry(dict):
    _missing_error = "Cannot use {key} as needed library {library} is not installed."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._missing = {}

    def register_missing(self, func: str, missing_library):
        self._missing[func] = missing_library
        self[func] = self._missing_error.format(key=func, library=missing_library)

    def __getitem__(self, key):
        if key in self._missing:
            raise ValueError(
                self._missing_error.format(key=key, library=self._missing[key])
            )
        return super().__getitem__(key)


_registry = Registry()


def register(_func=None, *, name=None, registry=_registry, **kwargs):
    def register_decorator(func):
        nonlocal registry
        nonlocal name
        if name is None:
            name = func.__name__
        else:
            func.__name__ = name
        for key, value in kwargs.items():
            setattr(func, key, value)
        registry[name] = func
        return func

    if _func is None:
        return register_decorator
    return register_decorator(_func)
