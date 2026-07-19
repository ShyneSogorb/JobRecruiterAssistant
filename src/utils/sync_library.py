
from functools import wraps


def synchronized_class(cls):
    for name, method in vars(cls).items():
        if name.startswith("_"):
            continue

        if not callable(method):
            continue

        @wraps(method)
        def wrapper(self, *args, __method=method, **kwargs):
            with self._lock:
                return __method(self, *args, **kwargs)

        setattr(cls, name, wrapper)

    return cls