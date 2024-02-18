from .utilites import print_color
from functools import wraps


class PyMikroTikExceptions(Exception):
    pass


class ConnectError(PyMikroTikExceptions):
    pass


class IpAddressFormatError(PyMikroTikExceptions):
    pass


class RouterError(PyMikroTikExceptions):
    pass


class InvalidSearchAttribute(PyMikroTikExceptions):
    pass


def exception_control(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        if args[0].connection._ignore_errors is False:
            return method(*args, **kwargs)
        try:
            return method(*args, **kwargs)
        except PyMikroTikExceptions as err:
            print_color(str(err), 'red')
            return err
    return wrapper
