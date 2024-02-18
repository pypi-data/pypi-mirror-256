from config import register


@register
def foo(a: int, b: str = "bar"):
    return f"{a} b"


@register(name="buzz", hello="world")
def goo(a: int, b: str = "bar"):
    return f"{a} b"
