# -*- coding:utf-8 -*-
""" unit test of utilfunc.

Here testing or_later() and my_glob() in rika.utilfunc.py
Other fucntions are tested by doctest.
"""

import unittest
import doctest
from contextlib import contextmanager
import os.path
import sys
_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(_SCRIPT_DIR, '..', '..'))
import rika

__author__ = 'suomesta'
__version__ = '1.0.0'


@contextmanager
def _hack_version_info(major, minor, micro):
    """ hack sys.version_info[].

    hacking sys.version_info[] to test or_later.
    this class shall be used in with-statement
    param[in]  major: replace to sys.version_info[0]. shall be int.
    param[in]  minor: replace to sys.version_info[1]. shall be int.
    param[in]  micro: replace to sys.version_info[2]. shall be int.
    """
    sys.version_info, org = (major, minor, micro), sys.version_info
    yield
    sys.version_info = org


class TestCheckType(unittest.TestCase):
    """ test check_type(). """
    def test_arguments_type_error1(self):
        """ test TypeError in precheck 1. """
        # wrong name
        self.assertRaises(TypeError,
                          rika.check_type, 1, dict())
        # wrong items
        self.assertRaises(TypeError,
                          rika.check_type, '', list())
        # wrong index
        self.assertRaises(TypeError,
                          rika.check_type, '', dict(), index=[])
        # wrong allow
        self.assertRaises(TypeError,
                          rika.check_type, '', dict(), allow=1)
        # wrong not_allow
        self.assertRaises(TypeError,
                          rika.check_type, '', dict(), not_allow=1)
        # wrong element_allow
        self.assertRaises(TypeError,
                          rika.check_type, '', dict(), element_allow=1)
        # wrong element_not_allow
        self.assertRaises(TypeError,
                          rika.check_type, '', dict(), element_not_allow=1)
        # wrong size
        self.assertRaises(TypeError,
                          rika.check_type, '', dict(), size=1)

    def test_arguments_type_error2(self):
        """ test TypeError in precheck 2. """
        a = [1, 2, 3]
        b = {'A': 10, 'B': 11}
        d = locals()
        # raise IndexError internal
        self.assertRaises(TypeError,
                          rika.check_type, 'a', d, index=3)
        # raise TypeError internal
        self.assertRaises(TypeError,
                          rika.check_type, 'a', d, index='0')
        # raise KeyError internal
        self.assertRaises(TypeError,
                          rika.check_type, 'b', d, index=3)

    def test_arguments_type_error3(self):
        """ test TypeError in precheck 3. """
        a = 1
        d = locals()
        # element_allow is not usable
        self.assertRaises(TypeError,
                          rika.check_type, 'a', d, element_allow=3)
        # element_not_allow is not usable
        self.assertRaises(TypeError,
                          rika.check_type, 'a', d, element_not_allow='0')
        # size is not usable
        self.assertRaises(TypeError,
                          rika.check_type, 'a', d, size=(0).__eq__)

    def test_index_works(self):
        """ test the argument 'index'. """
        wrap_check_type = rika.wrap_no_error(rika.check_type)

        # ---> a is list
        a = [True, 2, 3.0]
        d = locals()
        # raises no Exception
        self.assertRaises(rika.NoError,
                          wrap_check_type, 'a',
                          d, index=1, allow=int)
        self.assertRaises(rika.NoError,
                          wrap_check_type, 'a',
                          d, index=1, allow=(bool, int, float))
        # raises TypeError
        self.assertRaises(TypeError,
                          rika.check_type, 'a',
                          d, index=1, allow=float)
        self.assertRaises(TypeError,
                          rika.check_type, 'a',
                          d, index=1, allow=(bool, float))
        # confirm TypeError's text
        try:
            rika.check_type('a', d, index=1, allow=float)
        except TypeError as e:
            self.assertEqual('a[1]: float expected', str(e))
        try:
            rika.check_type('a', d, index=1, allow=(bool, float))
        except TypeError as e:
            self.assertEqual('a[1]: bool, float expected', str(e))
        # <--- a is list

        # ---> a is dict
        a = {'A': True, 'B': 11}
        d = locals()
        # raises no Exception
        self.assertRaises(rika.NoError,
                          wrap_check_type, 'a',
                          d, index='A', allow=bool)
        self.assertRaises(rika.NoError,
                          wrap_check_type, 'a',
                          d, index='B', allow=(bool, int, float))
        # raises TypeError
        self.assertRaises(TypeError,
                          rika.check_type, 'a',
                          d, index='A', allow=float)
        self.assertRaises(TypeError,
                          rika.check_type, 'a',
                          d, index='B', allow=(bool, float))
        # confirm TypeError's text
        try:
            rika.check_type('a', d, index='A', allow=float)
        except TypeError as e:
            self.assertEqual("a[A]: float expected", str(e))
        try:
            rika.check_type('a', d, index='B', allow=(bool, float))
        except TypeError as e:
            self.assertEqual("a[B]: bool, float expected", str(e))
        # <--- a is dict

    def test_allow_works(self):
        """ test the argument 'allow'. """
        wrap_check_type = rika.wrap_no_error(rika.check_type)

        a = 1
        d = locals()
        # raises no Exception
        self.assertRaises(rika.NoError,
                          wrap_check_type, 'a', d, allow=int)
        self.assertRaises(rika.NoError,
                          wrap_check_type, 'a', d, allow=(bool, int, float))
        # raises TypeError
        self.assertRaises(TypeError,
                          rika.check_type, 'a', d, allow=float)
        self.assertRaises(TypeError,
                          rika.check_type, 'a', d, allow=(bool, float))
        # confirm TypeError's text
        try:
            rika.check_type('a', d, allow=float)
        except TypeError as e:
            self.assertEqual('a: float expected', str(e))
        try:
            rika.check_type('a', d, allow=(bool, float))
        except TypeError as e:
            self.assertEqual('a: bool, float expected', str(e))

    def test_not_allow_works(self):
        """ test the argument 'not_allow'. """
        wrap_check_type = rika.wrap_no_error(rika.check_type)

        a = 1
        d = locals()
        # raises no Exception
        self.assertRaises(rika.NoError,
                          wrap_check_type, 'a', d, not_allow=bool)
        self.assertRaises(rika.NoError,
                          wrap_check_type, 'a', d, not_allow=(bool, float))
        # raises TypeError
        self.assertRaises(TypeError,
                          rika.check_type, 'a', d, not_allow=int)
        self.assertRaises(TypeError,
                          rika.check_type, 'a', d, not_allow=(int, float))
        # confirm TypeError's text
        try:
            rika.check_type('a', d, not_allow=int)
        except TypeError as e:
            self.assertEqual('a: int not allowed', str(e))
        try:
            rika.check_type('a', d, not_allow=(int, float))
        except TypeError as e:
            self.assertEqual('a: int, float not allowed', str(e))

    def test_element_allow_works(self):
        """ test the argument 'element_allow'. """
        wrap_check_type = rika.wrap_no_error(rika.check_type)

        # ---> a is list of ints
        a = [1, 2, 3]
        d = locals()
        # raises no Exception
        self.assertRaises(rika.NoError,
                          wrap_check_type,
                          'a', d, element_allow=int)
        self.assertRaises(rika.NoError,
                          wrap_check_type,
                          'a', d, element_allow=(bool, int, float))
        # raises TypeError
        self.assertRaises(TypeError,
                          rika.check_type,
                          'a', d, element_allow=float)
        self.assertRaises(TypeError,
                          rika.check_type,
                          'a', d, element_allow=(bool, float))
        # confirm TypeError's text
        try:
            rika.check_type('a', d, element_allow=float)
        except TypeError as e:
            self.assertEqual('in a: float expected', str(e))
        try:
            rika.check_type('a', d, element_allow=(bool, float))
        except TypeError as e:
            self.assertEqual('in a: bool, float expected', str(e))
        # <--- a is list of ints

        # ---> a is list of some types
        a = [True, 2, 3.0]
        d = locals()
        # raises no Exception
        self.assertRaises(rika.NoError,
                          wrap_check_type,
                          'a', d, element_allow=(bool, int, float))
        # raises TypeError
        self.assertRaises(TypeError,
                          rika.check_type,
                          'a', d, element_allow=(bool, float))
        # confirm TypeError's text
        try:
            rika.check_type('a', d, element_allow=(bool, float))
        except TypeError as e:
            self.assertEqual('in a: bool, float expected', str(e))
        # <--- a is list of some types

        # ---> a is empty list
        a = []
        d = locals()
        # raises no Exception
        self.assertRaises(rika.NoError,
                          wrap_check_type,
                          'a', d, element_allow=int)
        # <--- a is empty list

    def test_element_not_allow_works(self):
        """ test the argument 'element_not_allow'. """
        wrap_check_type = rika.wrap_no_error(rika.check_type)

        # ---> a is list of ints
        a = [1, 2, 3]
        d = locals()
        # raises no Exception
        self.assertRaises(rika.NoError,
                          wrap_check_type,
                          'a', d, element_not_allow=bool)
        self.assertRaises(rika.NoError,
                          wrap_check_type,
                          'a', d, element_not_allow=(bool, float))
        # raises TypeError
        self.assertRaises(TypeError,
                          rika.check_type,
                          'a', d, element_not_allow=int)
        self.assertRaises(TypeError,
                          rika.check_type,
                          'a', d, element_not_allow=(bool, int, float))
        # confirm TypeError's text
        try:
            rika.check_type('a', d, element_not_allow=int)
        except TypeError as e:
            self.assertEqual('in a: int not allowed', str(e))
        try:
            rika.check_type('a', d, element_not_allow=(bool, float))
        except TypeError as e:
            self.assertEqual('in a: bool, float expected', str(e))
        # <--- a is list of ints

        # ---> a is list of some types
        a = [True, 2, 3.0]
        d = locals()
        # raises no Exception
        self.assertRaises(rika.NoError,
                          wrap_check_type,
                          'a', d, element_not_allow=(list, tuple))
        # raises TypeError
        self.assertRaises(TypeError,
                          rika.check_type,
                          'a', d, element_not_allow=(bool, float))
        # confirm TypeError's text
        try:
            rika.check_type('a', d, element_not_allow=(bool, float))
        except TypeError as e:
            self.assertEqual('in a: bool, float not allowed', str(e))
        # <--- a is list of some types

        # ---> a is empty list
        a = []
        d = locals()
        # raises no Exception
        self.assertRaises(rika.NoError,
                          wrap_check_type,
                          'a', d, element_not_allow=int)
        # <--- a is empty list

    def test_size_works(self):
        """ test the argument 'size'. """
        wrap_check_type = rika.wrap_no_error(rika.check_type)

        a = [1, 2, 3]
        d = locals()
        # raises no Exception
        self.assertRaises(rika.NoError,
                          wrap_check_type, 'a', d, size=(3).__eq__)
        self.assertRaises(rika.NoError,
                          wrap_check_type, 'a', d, size=(0).__lt__)
        self.assertRaises(rika.NoError,
                          wrap_check_type, 'a', d, size=lambda x: 1 <= x < 10)
        # raises ValueError
        self.assertRaises(ValueError,
                          rika.check_type, 'a', d, size=(2).__eq__)
        self.assertRaises(ValueError,
                          rika.check_type, 'a', d, size=(1).__ge__)
        self.assertRaises(ValueError,
                          rika.check_type, 'a', d, size=lambda x: x % 2 == 0)
        # confirm ValueError's text
        try:
            rika.check_type('a', d, size=(2).__eq__)
        except ValueError as e:
            self.assertEqual('a: wrong length', str(e))


class TestLazyImport(unittest.TestCase):
    """ test LazyImport class. """
    def test_typeerror(self):
        """ test __init__ raises TypeError. """
        # raises TypeError
        self.assertRaises(TypeError, rika.LazyImport, 1)

    def test_importerror(self):
        """ test __getattr__ raises ImportError. """
        def wrap():
            lazy_import = rika.LazyImport('nomodule')
            lazy_import.attr

        # raises ImportError
        self.assertRaises(ImportError, wrap)

    def test_attributeerror(self):
        """ test __getattr__ raises AttributeError. """
        def wrap():
            lazy_import = rika.LazyImport('sys')
            lazy_import.noattribute

        # raises AttributeError
        self.assertRaises(AttributeError, wrap)

    def test_works_ok1(self):
        """ test LazyImport accesses sys.version_info. """
        sys_normal = __import__('sys')
        sys_lazy = rika.LazyImport('sys')

        self.assertTrue(sys_normal.version_info is sys_lazy.version_info)

    def test_works_ok2(self):
        """ test LazyImport accesses os.path.join. """
        os_normal = __import__('os')
        os_lazy = rika.LazyImport('os')

        self.assertTrue(os_normal.path.join is os_lazy.path.join)


class TestOrLater(unittest.TestCase):
    """ test or_later(). """
    def test_equal(self):
        """ test equal cases. """
        # all arguments are appointed
        with _hack_version_info(2, 7, 2):
            self.assertTrue(rika.or_later(2, 7, 2))
        # micro is not appointed
        with _hack_version_info(2, 7, 0):
            self.assertTrue(rika.or_later(2, 7))
        # minor is not appointed
        with _hack_version_info(3, 0, 2):
            self.assertTrue(rika.or_later(3, micro=2))

    def test_later(self):
        """ test later cases. """
        # tests with 2.7.2
        with _hack_version_info(2, 7, 2):
            self.assertTrue(rika.or_later(2, 7, 1))
            self.assertTrue(rika.or_later(2, 7))
            self.assertTrue(rika.or_later(2, 6, 2))
            self.assertTrue(rika.or_later(1, 7, 2))
        # tests with 3.3.3
        with _hack_version_info(3, 3, 3):
            self.assertTrue(rika.or_later(2, 3, 3))
            self.assertTrue(rika.or_later(2, 4))
            self.assertTrue(rika.or_later(2))
            self.assertTrue(rika.or_later(2, micro=3))

    def test_older(self):
        """ test older cases. """
        # tests with 2.7.2
        with _hack_version_info(2, 7, 2):
            self.assertFalse(rika.or_later(2, 7, 3))
            self.assertFalse(rika.or_later(2, 8, 2))
            self.assertFalse(rika.or_later(2, 8))
            self.assertFalse(rika.or_later(3, 7, 2))
            self.assertFalse(rika.or_later(3, 7))
            self.assertFalse(rika.or_later(3, 6))
            self.assertFalse(rika.or_later(3, micro=2))
            self.assertFalse(rika.or_later(3))

    def test_exception(self):
        """ test raised exception cases. """
        # wrong major
        self.assertRaises(TypeError, rika.or_later, None, 0, 0)
        # wrong minor
        self.assertRaises(TypeError, rika.or_later, 0, 1.0, 0)
        # wrong micro
        self.assertRaises(TypeError, rika.or_later, 0, 0, '0')


class TestMyGlob(unittest.TestCase):
    """ test my_glob().

    all tests are done on data/my_glob folder.
    """
    def test_aster_false(self):
        """ test with '*' and recursive is off. """
        join = os.path.join
        root_dir = join('data', 'utilfunc', 'my_glob')
        required = ([
            join(root_dir, 'a.txt'),
            join(root_dir, 'b.log'),
            join(root_dir, 'New document.txt'),
            join(root_dir, 'Uusi tekstiasiakirja.txt'),
        ])
        result = rika.my_glob(root_dir, '*', False)
        self.assertEqual(required, result)

    def test_aster_true(self):
        """ test with '*' and recursive is on. """
        join = os.path.join
        root_dir = join('data', 'utilfunc', 'my_glob')
        required = ([
            join(root_dir, 'a.txt'),
            join(root_dir, 'b.log'),
            join(root_dir, 'New document.txt'),
            join(root_dir, 'Uusi tekstiasiakirja.txt'),
            join(root_dir, '1st', 'a.txt'),
            join(root_dir, '1st', 'b.log'),
            join(root_dir, '1st', 'New document.txt'),
            join(root_dir, '1st', 'Uusi tekstiasiakirja - kopio.txt'),
            join(root_dir, '1st', 'Uusi tekstiasiakirja.txt'),
            join(root_dir, '1st', '2nd', 'New document.txt'),
            join(root_dir, '1st', '2nd', 'Uusi tekstiasiakirja.txt'),
        ])
        result = rika.my_glob(root_dir, '*', True)
        self.assertEqual(required, result)

    def test_text_true(self):
        """ test with '*.txt' and recursive is on. """
        join = os.path.join
        root_dir = join('data', 'utilfunc', 'my_glob')
        required = ([
            join(root_dir, 'a.txt'),
            join(root_dir, 'New document.txt'),
            join(root_dir, 'Uusi tekstiasiakirja.txt'),
            join(root_dir, '1st', 'a.txt'),
            join(root_dir, '1st', 'New document.txt'),
            join(root_dir, '1st', 'Uusi tekstiasiakirja - kopio.txt'),
            join(root_dir, '1st', 'Uusi tekstiasiakirja.txt'),
            join(root_dir, '1st', '2nd', 'New document.txt'),
            join(root_dir, '1st', '2nd', 'Uusi tekstiasiakirja.txt'),
        ])
        result = rika.my_glob(root_dir, '*.txt', True)
        self.assertEqual(required, result)

    def test_uusi_true(self):
        """ test with 'U*' and recursive is on. """
        join = os.path.join
        root_dir = join('data', 'utilfunc', 'my_glob')
        required = ([
            join(root_dir, 'Uusi tekstiasiakirja.txt'),
            join(root_dir, '1st', 'Uusi tekstiasiakirja - kopio.txt'),
            join(root_dir, '1st', 'Uusi tekstiasiakirja.txt'),
            join(root_dir, '1st', '2nd', 'Uusi tekstiasiakirja.txt'),
        ])
        result = rika.my_glob(root_dir, 'Uusi*', True)
        self.assertEqual(required, result)

    def test_exception(self):
        """ test wrong argumens. """
        self.assertRaises(TypeError, rika.my_glob, 1, '*', False)
        self.assertRaises(TypeError, rika.my_glob, '.', 1, False)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocTestSuite(rika.utils))
    unittest.TextTestRunner(verbosity=2).run(suite)

    unittest.main()
