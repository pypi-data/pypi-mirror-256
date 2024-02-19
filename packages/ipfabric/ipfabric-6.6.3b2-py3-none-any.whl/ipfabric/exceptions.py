from warnings import warn


def deprecated_args_decorator(version: str, arg_type=None, no_args: bool = True):  # noqa: C901

    def inner(func):

        fname = func.__name__

        def wrapper(*args, **kwargs):
            if arg_type:
                arg_types = [arg_type] if isinstance(arg_type, str) else arg_type
                msg = (
                    f"`{fname}()` no longer accepts parameter of `{arg_type}` and will be removed in version {version}."
                )
                if args:
                    for arg in args:
                        if type(arg).__name__ in arg_types:
                            warn(msg, DeprecationWarning, stacklevel=2)
                if kwargs:
                    for arg in kwargs.values():
                        if type(arg).__name__ in arg_types:
                            warn(msg, DeprecationWarning, stacklevel=2)
            if no_args and (len(args) > 1 or kwargs):
                warn(
                    f"`{fname}()` parameters are deprecated and will be removed in version {version}.",
                    DeprecationWarning,
                    stacklevel=2,
                )
            return func(*args, **kwargs)

        return wrapper

    return inner
