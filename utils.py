# -*- coding:utf-8 -*-
""" Utility functions.

Defines some utility functions.
"""

__author__ = 'suomesta'
__version__ = '1.0.0'

import collections.abc
sys = None  # lazy import
fnmatch = None  # lazy import
os = None  # lazy import


def check_type(name, items, index=None, allow=None, not_allow=None,
               element_allow=None, element_not_allow=None, size=None):
    """ type checker

    Check type. If wrong type is found, then raise TypeError.
    This functions intends to be used to check arguments' type in a function.
    param[in]  name: name of value. shall be str.
                     Normally this is the name of local valuable.
    param[in]  items: valuables in dict. shall be dict.
                      Normally this is locals().
    param[in]  index: it could be appointed to index of value.
                      items[name][index] shall be accessable.
    param[in]  allow: allowed type of value. shall be type or tuple of types.
    param[in]  not_allow: not allowed type of value. shall be type or tuple
                          of types.
    param[in]  element_allow: type or tuple of types for checking elements
                              of value. if len(value) == 0, then always OK
    param[in]  element_not_allow: type or tuple of types for checking elements
                                  of value. if len(value) == 0, then always OK
    param[in]  size: appointed size condition of value. this shall be function
                     whose argument is len(value).
                     Only this condition raises ValueError (not TypeError).
                     if len(value) == 12 is required, then (12).__eq__
                     is appropreate.
                     if len(value) > 0 is required, then (0).__lt__
                     is appropreate.
                     lambda is useful for this argument.
    raise      TypeError: case1: parameter is wrong
                          case2: value is not satisfied required condition
               ValueError: value does not match with size()
    note       Following doctest shows typical usage. More detailed test is
               done in test script

    doctest ---
    >>> a = 1
    >>> check_type('a', locals(), allow=int)
    >>> check_type('a', locals(), allow=float)
    Traceback (most recent call last):
       ...
    TypeError: a: float expected

    >>> a = None
    >>> check_type('a', locals(), allow=type(None))

    >>> a = True
    >>> check_type('a', locals(), allow=int, not_allow=bool)
    Traceback (most recent call last):
       ...
    TypeError: a: bool not allowed

    >>> a = [1, 2, 3]
    >>> check_type('a', locals(), allow=list)
    >>> check_type('a', locals(), element_allow=int)
    >>> check_type('a', locals(), element_not_allow=int)
    Traceback (most recent call last):
       ...
    TypeError: in a: int not allowed

    >>> a = (1, 2.0)
    >>> check_type('a', locals(), index=1, allow=float)
    >>> a = {'a': 10, 'b': 11, 'c': 12}
    >>> check_type('a', locals(), index='b', allow=int)

    >>> a = [1, 2, 3]
    >>> check_type('a', locals(), size=(3).__eq__)
    >>> check_type('a', locals(), size=(0).__lt__)
    >>> check_type('a', locals(), size=(2).__ge__)
    Traceback (most recent call last):
       ...
    ValueError: a: wrong length
    """
    def is_type(arg):
        """ inner function to check the arg is type or tuple of types """
        if isinstance(arg, type):
            return True
        else:
            return isinstance(arg, tuple) and all(is_type(i) for i in arg)

    def type_names(arg, buf=None):
        """ inner function to get list of str of type or tuple of types """
        buf = [] if buf is None else buf
        if isinstance(arg, type):
            buf.append(arg.__name__)
        else:
            for i in arg:
                type_names(i, buf)
        return buf

    # ---> precheck (1 of 3)
    if not (isinstance(name, str) and
            isinstance(items, dict) and
            (index is None or isinstance(index, collections.abc.Hashable)) and
            (allow is None or is_type(allow)) and
            (not_allow is None or is_type(not_allow)) and
            (element_not_allow is None or is_type(element_not_allow)) and
            (element_allow is None or is_type(element_allow)) and
            (size is None or isinstance(size, collections.abc.Callable))):
        raise TypeError('Incorrect parameter for check_type()')
    # <--- precheck (1 of 3)

    # ---> precheck (2 of 3)
    # get value
    try:
        val = items[name] if index is None else items[name][index]
        valname = name if index is None else (name + '[' + str(index) + ']')
    except (IndexError, KeyError, TypeError):
        raise TypeError('Incorrect parameter for check_type()')
    # <--- precheck (2 of 3)

    # ---> precheck (3 of 3)
    if element_allow is not None or element_not_allow is not None:
        if not isinstance(val, collections.abc.Iterable):
            raise TypeError('Incorrect parameter for check_type()')
    if size is not None:
        if not isinstance(val, collections.abc.Sized):
            raise TypeError('Incorrect parameter for check_type()')
    # <--- precheck (3 of 3)

    if allow is not None:
        if not isinstance(val, allow):
            types = ', '.join(type_names(allow))
            msg = '{0}: {1} expected'.format(valname, types)
            raise TypeError(msg)

    if not_allow is not None:
        if isinstance(val, not_allow):
            types = ', '.join(type_names(not_allow))
            msg = '{0}: {1} not allowed'.format(valname, types)
            raise TypeError(msg)

    if element_allow is not None:
        if not all(isinstance(i, element_allow) for i in val):
            types = ', '.join(type_names(element_allow))
            msg = 'in {0}: {1} expected'.format(valname, types)
            raise TypeError(msg)

    if element_not_allow is not None:
        if any(isinstance(i, element_not_allow) for i in val):
            types = ', '.join(type_names(element_not_allow))
            msg = 'in {0}: {1} not allowed'.format(valname, types)
            raise TypeError(msg)

    if size is not None:
        if not size(len(val)):
            msg = '{0}: wrong length'.format(valname)
            raise ValueError(msg)


class LazyImport(object):
    """ Lazy module loading

    This class does lazy import.
    This class is based on sample source code in Python Standard Library (by
    Fredrik Lundh, publisher: O'Reilly Media)

    typical usage is,
    sys = LazyImport('sys')
    print(sys.version_info)
    """
    __slots__ = ('__name', '__module')

    def __init__(self, name):
        """ initialize.

        Prepare to import, but not import here.
        param[in]  name: appointed module name. It shall be str.
        raise      TypeError: if argument is not str
        """
        check_type('name', locals(), allow=str)

        self.__name = name
        self.__module = None

    def __getattr__(self, attr):
        """ customized __getattr__

        return appointed attribute. import module if it has not been imported.
        param[in]  attr: appointed attribute name. it is always str.
        raise      ImportError: when module is not found
                   AttributeError: when attribute is not found
        """
        if self.__module is None:
            self.__module = __import__(self.__name)
        return getattr(self.__module, attr)


def is_int(i):
    """ int checker

    Check if the argument is pure int or not. bool returns False. The check
    depends on isinstance().
    param[in]  i: appointed data.
    return     If i is pure int (not including bool), then True. Else, False.

    doctest ---
    >>> is_int(0)
    True
    >>> is_int(-1)
    True
    >>> is_int(999999999999999)
    True
    >>> is_int(True)
    False
    >>> is_int(1.0)
    False
    >>> is_int('1')
    False
    """
    return isinstance(i, int) and not isinstance(i, bool)


def is_ascii(string):
    """ ascii checker

    Check if the argument is ASCII format or not. The check depends on
    str.encode().
    param[in]  string: appointed string data. It should be str.
    return     If string is ASCII format, then True. Else, False.
    raise      TypeError: if argument is not str

    doctest ---
    >>> is_ascii('ascii')
    True
    >>> is_ascii('äscii')
    False
    >>> is_ascii('')
    True
    >>> is_ascii(0)
    Traceback (most recent call last):
       ...
    TypeError: string: str expected
    """
    check_type('string', locals(), allow=str)

    try:
        string.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False


def is_float(string):
    """ float checker

    Check if the argument is float string or not. The check depends on
    float().
    param[in]  string: appointed string data. It should be str.
    return     If string can be converted into float, then True. Else, False.
    raise      TypeError: if argument is not str

    doctest ---
    >>> is_float('1.5')
    True
    >>> is_float('1')
    True
    >>> is_float('abc')
    False
    >>> is_float('')
    False
    >>> is_float(1.5)
    Traceback (most recent call last):
       ...
    TypeError: string: str expected
    """
    check_type('string', locals(), allow=str)

    try:
        float(string)
        return True
    except ValueError:
        return False


def remove_overlaps(src):
    """ Remove duplex items

    Remove duplex items from sliceable object, and return new list.
    param[in]  src: source data. shall be sliceable
    return     A list which does not contain duplex item. the order of items
               are kept from source data.
    raise      TypeError: if src is not sliceable
    note       when src is bytes, result is little bit strange. the result
               depends on set().

    doctest ---
    >>> remove_overlaps([1,7,3,3,4,5,3,6,7]) == [1,7,3,4,5,6]
    True
    >>> remove_overlaps([1,1,7,7,1,3]) == [1,3,7]
    False
    >>> remove_overlaps((1,7,3,3,4,5,3,6,7)) == [1,7,3,4,5,6]
    True
    >>> remove_overlaps('setter') == ['s','e','t','r']
    True
    >>> remove_overlaps(b'ACBAB') == [65,67,66]
    True
    >>> remove_overlaps(bytearray(range(3))) == [0,1,2]
    True
    >>> remove_overlaps(range(5)) == [0,1,2,3,4]
    True
    >>> remove_overlaps([]) == []
    True
    >>> remove_overlaps(1)
    Traceback (most recent call last):
        ...
    TypeError: src: Sequence expected
    """
    check_type('src', locals(), allow=collections.abc.Sequence)

    return sorted(set(src), key=src.index)


def divide(src, length):
    """ Divide sequence

    Divide one sequence object into list of fixed length object.
    param[in]  src: source object. shall be sliceable
    param[in]  length: fixed length. shall be int (> 0)
    return     A list of object whose length is same (except last one).
    raise      TypeError: if src is not sliceable or length is not int
               ValueError: if length is 0

    doctest ---
    >>> divide('111222333444', 3) == ['111','222','333','444']
    True
    >>> divide('xyzxyzxyzx', 3) == ['xyz','xyz','xyz','x']
    True
    >>> divide([1,2,3,4,5], 2) == [[1,2],[3,4],[5]]
    True
    >>> divide((1,2,3,4,5), 1) == [(1,),(2,),(3,),(4,),(5,)]
    True
    >>> divide(b'111222333444', 3) == [b'111',b'222',b'333',b'444']
    True
    >>> divide(bytearray(4), 3) == [bytearray(3),bytearray(1)]
    True
    >>> divide(range(5), 2) == [range(2),range(2,4),range(4,5)]
    True
    >>> divide('', 3) == []
    True
    >>> divide(10, 0)
    Traceback (most recent call last):
        ...
    TypeError: src: Sequence expected
    >>> divide('xyzxyzxyzx', -1)
    []
    >>> divide('xyzxyzxyzx', 1.0)
    Traceback (most recent call last):
        ...
    TypeError: length: int expected
    >>> divide('xyzxyzxyzx', 0)
    Traceback (most recent call last):
        ...
    ValueError: length: must not be zero
    """
    check_type('src', locals(), allow=collections.abc.Sequence)
    check_type('length', locals(), allow=int)
    if length == 0:
        raise ValueError('length: must not be zero')

    return [src[i:i+length] for i in range(0, len(src), length)]


def count_if(target, predicate=bool):
    """ Count items

    Count items which satisfies condition.
    The basic idea is from c++ std::count_if().
    param[in]  target: target of counting. It shall be iterable.
    param[in]  predicate: function to filter by condition.
                          Its return value shall be bool.
    return     The number of items which satisfies condition.
    raise      TypeError: if target is not iterable

    doctest ---
    >>> count_if([0, 1, 2, 3, 0, 1, 2, 3, 0])
    6
    >>> count_if([0, 1, 2, 3, 0, 1, 2, 3, 0], lambda x: x % 2 == 0)
    5
    >>> count_if(['', 'a', '', 'b', ''])
    2
    >>> count_if(10)
    Traceback (most recent call last):
        ...
    TypeError: target: Iterable expected
    """
    check_type('target', locals(), allow=collections.abc.Iterable)
    check_type('predicate', locals(), allow=collections.abc.Callable)

    return sum(predicate(i) for i in target)


def or_later(major, minor=0, micro=0):
    """ pyhon version checker.

    The pyhon version now using is same or later than appointed version.
    param[in]  major: checked version number. shall be int.
    param[in]  minor: checked version number. shall be int.
    param[in]  micro: checked version number. shall be int.
    return     True: the version now using is same or later than arguments
               False: the version now using is former than arguments
    raise      TypeError: if one of arguments is not int
    example    If you use python '3.2.1' and argment is (3, 2, 0),
               then return True
    """
    # lazy import
    global sys
    if sys is None:
        sys = __import__('sys')

    check_type('major', locals(), allow=int)
    check_type('minor', locals(), allow=int)
    check_type('micro', locals(), allow=int)

    return sys.version_info >= (major, minor, micro)


def my_glob(root_dir='.', pattern='*', recursive=False):
    """ glob with recursive mode.

    Get file list on root directory. this method supports recursive mode.
    param[in]  root_dir: root directory name in str
    param[in]  pattern: pattern for filtering. shall be str
    param[in]  recursive: recursive or not. shall be bool
    return     gotten file name list. the name starts with root_dir.
    raise      TypeError: if root_dir or pattern is not str
    """
    # lazy import
    global fnmatch
    if fnmatch is None:
        fnmatch = __import__('fnmatch')
    global os
    if os is None:
        os = __import__('os')

    check_type('root_dir', locals(), allow=str)
    check_type('pattern', locals(), allow=str)

    results = []
    append = results.append

    for loop_dir, _, files in os.walk(root_dir, topdown=True):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                append(os.path.join(loop_dir, file))

        if not recursive:
            break

    return results
