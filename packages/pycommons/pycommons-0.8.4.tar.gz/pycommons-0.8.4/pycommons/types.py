"""Some basic type handling routines."""
from typing import Any, Final, Iterable


def type_name(tpe: type | None) -> str:
    """
    Convert a type to a string which represents its name.

    :param tpe: the type
    :returns: the string

    >>> type_name(None)
    'None'
    >>> type_name(type(None))
    'None'
    >>> type_name(int)
    'int'
    >>> from pycommons.io.path import Path
    >>> type_name(Path)
    'pycommons.io.path.Path'
    >>> from typing import Callable
    >>> type_name(Callable)
    'typing.Callable'
    >>> from typing import Callable as Ca
    >>> type_name(Ca)
    'typing.Callable'
    >>> from typing import Callable as Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    >>> type_name(Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa)
    'typing.Callable'
    >>> import typing as ttttttttttttttttttttttttttttttttttttttttttt
    >>> type_name(ttttttttttttttttttttttttttttttttttttttttttt.Callable)
    'typing.Callable'
    """
    if tpe is None:
        return "None"
    c1: str = str(tpe)
    if c1.startswith("<class '"):
        c1 = c1[8:-2]
    if c1 == "NoneType":
        return "None"
    if hasattr(tpe, "__qualname__"):
        c2: str = tpe.__qualname__
        if hasattr(tpe, "__module__"):
            module = tpe.__module__
            if (module is not None) and (module != "builtins"):
                c2 = f"{module}.{c2}"
        if len(c2) >= len(c1):
            return c2
    return c1  # will probably never happen


def type_name_of(obj: Any) -> str:
    """
    Get the fully-qualified class name of an object.

    :param obj: the object
    :returns: the fully-qualified class name of the object

    >>> from pycommons.io.path import Path
    >>> type_name_of(Path)
    'type'
    >>> type_name_of(Path.file(__file__))
    'pycommons.io.path.Path'
    >>> type_name_of(None)
    'None'
    >>> type_name_of(int)
    'type'
    >>> type_name_of(print)
    'builtin_function_or_method'
    >>> from typing import Callable
    >>> type_name_of(Callable)
    'typing._CallableType'
    >>> from math import sin
    >>> type_name_of(sin)
    'builtin_function_or_method'
    >>> import pycommons.io as iox
    >>> type_name_of(iox)
    'module'
    """
    if obj is None:
        return "None"
    if isinstance(obj, type):
        return "type"
    return type_name(type(obj))


def type_error(obj: Any, name: str,
               expected: None | type | Iterable[type] = None,
               call: bool = False) -> ValueError | TypeError:
    """
    Create an error to raise if a type did not fit.

    :param obj: the object that is of the wrong type
    :param name: the name of the object
    :param expected: the expected types (or `None`)
    :param call: the object should have been callable?
    :returns: a :class:`TypeError` with a descriptive information

    >>> type_error(1.3, "var", int)
    TypeError("var should be an instance of int but is float, namely '1.3'.")
    >>> type_error("x", "z", (int, float)).args[0]
    "z should be an instance of any in {float, int} but is str, namely 'x'."
    >>> type_error("x", "z", (int, float, None)).args[0]
    "z should be an instance of any in {None, float, int} but is str, namely \
'x'."
    >>> type_error("x", "z", (int, float, type(None))).args[0]
    "z should be an instance of any in {None, float, int} but is str, namely \
'x'."
    >>> type_error("f", "q", call=True).args[0]
    "q should be a callable but is str, namely 'f'."
    >>> type_error("1", "2", bool, call=True).args[0]
    "2 should be an instance of bool or a callable but is str, namely '1'."
    >>> type_error(None, "x", str)
    TypeError('x should be an instance of str but is None.')
    """
    exp: str = ""
    if isinstance(expected, Iterable):
        exp = ", ".join(sorted(map(type_name, expected)))
        exp = f"an instance of any in {{{exp}}}"
    elif expected is not None:
        exp = f"an instance of {type_name(expected)}"
    if call:
        exp = f"{exp} or a callable" if exp else "a callable"

    message: Final[str] = f"{name} should be {exp} but is None." \
        if obj is None else \
        (f"{name} should be {exp} but is {type_name_of(obj)}, "
         f"namely {str(obj)!r}.")

    return TypeError(message)


def check_int_range(val: Any, name: str | None = None,
                    min_value: int | float = 0,
                    max_value: int | float = 1_000_000_000) -> int:
    """
    Check whether a value `val` is an integer in a given range.

    Via type annotation, this method actually accepts a value `val` of any
    type as input. However, if `val` is not an instance of `int`, it will
    throw an error. Also, if `val` is not in the prescribed range, it will
    throw an error, too. By default, the range is `0...1_000_000_000`.

    I noticed that often, we think that  only want to check a lower limit
    for `val`, e.g., that a number of threads or a population size should be
    `val > 0`. However, in such cases, there also always a reasonable upper
    limits. We never actually want an EA to have a population larger than,
    say, 1_000_000_000. That would make no sense. So indeed, whenever we have
    a lower limit for a parameter, we also should have an upper limit
    resulting from physical constraints. 1_000_000_000 is a reasonably sane
    upper limit in many situations. If we need smaller or larger limits, we
    can of course specify them.

    Notice that there is one strange border case: In Python, `bool` is a
    subtype of `int`, where `True` has value `1` and `False` has value `0`.
    See <https://docs.python.org/3/library/functions.html#bool>.
    We therefore treat `bool` values indeed as instances of `int`.

    :param val: the value to check
    :param name: the name of the value, or `None`
    :param min_value: the minimum permitted value
    :param max_value: the maximum permitted value
    :returns: `val` if everything is OK
    :raises TypeError: if `val` is not an `int`
    :raises ValueError: if `val` is an `int` but outside the prescribed range

    >>> try:
    ...   print(check_int_range(12, min_value=7, max_value=13))
    ... except (ValueError, TypeError) as err:
    ...   print(err)
    12

    >>> try:
    ...   print(check_int_range(123, min_value=7, max_value=13))
    ... except (ValueError, TypeError) as err:
    ...   print(err)
    ...   print(err.__class__)
    Value=123 is invalid, must be in 7..13.
    <class 'ValueError'>

    >>> try:
    ...   print(check_int_range(5.0, name="ThisIsFloat"))
    ... except (ValueError, TypeError) as err:
    ...   print(err)
    ...   print(err.__class__)
    ThisIsFloat should be an instance of int but is float, namely '5.0'.
    <class 'TypeError'>

    The behavior in the border case of `bool` instances actually also being
    instances of `int`:

    >>> check_int_range(True, "true", 0, 2)
    True

    >>> check_int_range(False, "false", 0, 2)
    False

    >>> try:
    ...   print(check_int_range(True, min_value=7, max_value=13))
    ... except (ValueError, TypeError) as err:
    ...   print(err)
    ...   print(err.__class__)
    Value=True is invalid, must be in 7..13.
    <class 'ValueError'>
    """
    if not isinstance(val, int):
        raise type_error(val, "value" if name is None else name, int)
    if min_value <= val <= max_value:
        return val
    raise ValueError(f"{'Value' if name is None else name}={val!r} is "
                     f"invalid, must be in {min_value}..{max_value}.")


def check_to_int_range(val: Any, name: str | None = None,
                       min_value: int | float = 0,
                       max_value: int | float = 1_000_000_000) -> int:
    """
    Check whether a value `val` can be converted an integer in a given range.

    :param val: the value to convert via `int(...)` and then to check
    :param name: the name of the value, or `None`
    :param min_value: the minimum permitted value
    :param max_value: the maximum permitted value
    :returns: `val` if everything is OK
    :raises TypeError: if `val` is `None`
    :raises ValueError: if `val` is not `None` but can either not be converted
       to an `int` or to an `int` outside the prescribed range

    >>> try:
    ...   print(check_to_int_range(12))
    ... except (ValueError, TypeError) as err:
    ...   print(err)
    12

    >>> try:
    ...   print(check_to_int_range(12.0))
    ... except (ValueError, TypeError) as err:
    ...   print(err)
    12

    >>> try:
    ...   print(check_to_int_range("12"))
    ... except (ValueError, TypeError) as err:
    ...   print(err)
    12

    >>> try:
    ...   print(check_to_int_range("A"))
    ... except (ValueError, TypeError) as err:
    ...   print(err)
    ...   print(err.__class__)
    Cannot convert value='A' to int, let alone in range 0..1000000000.
    <class 'ValueError'>

    >>> try:
    ...   print(check_to_int_range(None))
    ... except (ValueError, TypeError) as err:
    ...   print(err)
    ...   print(err.__class__)
    Cannot convert value=None to int, let alone in range 0..1000000000.
    <class 'TypeError'>
    """
    try:
        conv = int(val)
    except (ValueError, TypeError) as errx:
        raise (ValueError if isinstance(errx, ValueError) else TypeError)(
            f"Cannot convert {'value' if name is None else name}={val!r} "
            f"to int, let alone in range {min_value}..{max_value}.") from errx
    return check_int_range(conv, name, min_value, max_value)
