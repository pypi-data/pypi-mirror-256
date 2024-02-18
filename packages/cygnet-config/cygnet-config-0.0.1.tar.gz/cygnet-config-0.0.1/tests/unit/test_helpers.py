from config.helpers import partial


def foo(x, y, z, **kwargs):
    return dict(x=x, y=y, z=z, kwargs=kwargs)


class Test_partial:
    def test_passes_kwargs_to_func(self):
        f = partial(foo, z=4, bar="buzz")
        out = f(2, 3)
        assert out == dict(x=2, y=3, z=4, kwargs=dict(bar="buzz"))

    def test_passes_args_to_func(self):
        f = partial(foo, args=(2, 3), bar="buzz")
        out = f(4)
        assert out == dict(x=2, y=3, z=4, kwargs=dict(bar="buzz"))
