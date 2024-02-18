import typing as t
from functools import partial as pypartial

from ._registry import register


@register
def partial(function: t.Callable, args: tuple = tuple(), **kwargs):
    return pypartial(function, *args, **kwargs)
