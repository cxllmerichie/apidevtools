import functools
import inspect


inf: int = 2147483647


def asyncinit(obj):
    async def _new(cls, *args, **kwargs):
        return object.__new__(cls)

    def force_async(fn):
        if inspect.iscoroutinefunction(fn):
            return fn

        async def wrapped(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapped

    if not inspect.isclass(obj):
        raise ValueError("decorated object must be a class")
    cls_new = _new if obj.__new__ is object.__new__ else force_async(obj.__new__)

    @functools.wraps(obj.__new__)
    async def new(cls, *args, **kwargs):
        self = await cls_new(cls, *args, **kwargs)
        await force_async(self.__init__)(*args, **kwargs)
        return self
    obj.__new__ = new
    return obj
