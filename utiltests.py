# -*- coding:utf-8 -*-
""" Utility class and function for test.

Defines some utility classess and functions. These are useful for testing.
"""

import sys
import io
import tempfile
import os
from contextlib import contextmanager
import rika

__author__ = 'T.Oda FEC'
__version__ = '1.1.0'


class NoError(Exception):
    """ Exception, which indicates no error.

    It is intended to use assertRaises(NoError, ...) of unittest to confirm
    other error is not raised. More details, refer docs in wrap_no_error().
    """
    pass


def wrap_no_error(func):
    """ wrapper function to raise NoError

    call 'func()' and raise NoError.
    It is intended to use assertRaises(NoError, wrap_no_error(func), ...)
    of unittest.
    param[in]  func: function to be wrapped
    return     wrapped function.

    typical usage is,
    wrapped = wrap_no_error(my_function)
    assertRaises(NoError, wrapped, arg1, arg2)
    """
    from collections.abc import Callable
    rika.check_type('func', locals(), allow=Callable)

    def inner(*args, **kwargs):
        """ inner function to wrap"""
        func(*args, **kwargs)
        raise NoError

    return inner


class PrintHack(object):
    """ hacking print (sys.stdout)

    hacking print (sys.stdout) to test.
    this class shall be used in with-statement.

    typical usage is,
    with PrintHack() as hack:
        print('abc')
    self.assertEqual(hack.get(), 'abc\n')
    """
    __slots__ = ('__io', '__tmp')

    def __init__(self):
        """ __init__

        import sys and io (this is lazy import).
        create self.__io as io.StringIO.
        self.__tmp is for store sys.stdout
        """
        # set attributes
        self.__io = io.StringIO()
        self.__tmp = None

    def __enter__(self):
        """ __enter__

        swap sys.stdout and self.__hold.
        now sys.stdout becomes io.StringIO.
        """
        self.__tmp, sys.stdout = sys.stdout, self.__io
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ __exit__

        swap again sys.stdout and self.__hold.
        now sys.stdout is restored.
        """
        self.__tmp, sys.stdout = None, self.__tmp

    def get(self):
        """ get string

        get string from io.StringIO object.
        return    value of io.StringIO
        """
        return self.__io.getvalue()

    def reset(self):
        """ reset io.StringIO

        reset io.StringIO.
        """
        self.__io.truncate(0)
        self.__io.seek(0)


@contextmanager
def argv_hack(argv):
    """ hacking sys.argv

    hacking sys.argv to test.
    this function shall be used in with-statement.
    param[in]  argv: test data in place of sys.argv. shall be list of str.
    raise      TypeError: when argv is not list of str

    typical usage is,
    test_argv = ['sample', '--help']
    with argv_hack(test_argv):
        # do something
    """
    # check TypeError
    rika.check_type('argv', locals(), allow=list, element_allow=str)

    # swap argv
    sys.argv, stored = argv[::], sys.argv[::]
    yield
    # restore
    sys.argv = stored[::]


class ScopedFile(object):
    """ temporary file in with-statement

    create temporary file and support some function and automatic remove.
    this class shall be used in with-statement.

    typical usage is,
    with ScopedFile() as tmp:
        tmp.write(b'test data')
        some_function_to_file(tmp.path)
    """
    __slots__ = ('__mkstemp_args', '__fh', '__path')

    def __init__(self, suffix='', prefix='tmp'):
        """ __init__

        import tempfile and os (this is lazy import).
        create self.__mkstemp_args for the arguments of mkstemp().
        self.__fh and self.__path are for mkstemp()'s return value.
        param[in]  suffix: suffix for temp file name. shall be str
        param[in]  prefix: prefix for temp file name. shall be str
        """
        # check TypeError
        rika.check_type('suffix', locals(), allow=str)
        rika.check_type('prefix', locals(), allow=str)

        # set attributes
        self.__mkstemp_args = (suffix, prefix, None, False)
        self.__fh = None
        self.__path = None

    def __enter__(self):
        """ __enter__

        create temporary file.
        raise      OSError: depends on tempfile.mkstemp()
        """
        self.__fh, self.__path = tempfile.mkstemp(*self.__mkstemp_args)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ __exit__

        remove temporary file.
        """
        os.close(self.__fh)
        os.remove(self.__path)
        self.__fh = None
        self.__path = None

    @property
    def path(self):
        """ getter of self.__path """
        return self.__path

    def read(self, binarymode=False):
        """ read from temporary file

        call read() to temporary file.
        return     result of read()
        raise      RuntimeError: used out of with scope
                   OSError: depends on open() and file.read()
        """
        if self.__fh is None or self.__path is None:
            raise RuntimeError('ScopedFile is used out of with scope')

        mode = 'rb' if binarymode else 'r'
        with open(self.__path, mode) as file:
            return file.read()

    def write(self, data, binarymode=False):
        """ write to temporary file

        call write() to temporary file.
        param[in]  data: data to be written.
        return     result of write()
        raise      RuntimeError: used out of with scope
                   OSError: depends on open() and file.write()
        """
        if self.__fh is None or self.__path is None:
            raise RuntimeError('ScopedFile is used out of with scope')

        mode = 'wb' if binarymode else 'w'
        with open(self.__path, mode) as file:
            return file.write(data)
