# -*- coding:utf-8 -*-
""" unit test of utilfunc.

Here testing PrintHack and ScopedFile.
"""

import unittest
import os.path
import sys
_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(_SCRIPT_DIR, '..', '..'))
import rika

__author__ = 'suomesta'
__version__ = '1.0.0'


class TestWrapNoError(unittest.TestCase):
    """ test wrap_no_error-function."""
    def test_type_error(self):
        """ test TypeError is raised when the argument is not function. """
        self.assertRaises(TypeError, rika.wrap_no_error, 1)

    def test_no_error_raised_with_no_argument(self):
        """ test NoError is raised. function has no argument. """
        def func():
            """ function, which has no argument and not raise Exception. """
            pass

        wrapped = rika.wrap_no_error(func)
        self.assertRaises(rika.NoError, wrapped)

    def test_no_error_not_raised_with_no_argument(self):
        """ test NoError is not raised. function has not argument. """
        def func():
            """ function, which has no argument and raises RuntimeError. """
            raise RuntimeError

        wrapped = rika.wrap_no_error(func)
        self.assertRaises(RuntimeError, wrapped)

    def test_no_error_raised_with_two_arguments(self):
        """ test NoError is raised. function has 2 arguments. """
        def greater(a, b):
            """ function, which has 2 arguments and may raise ValueError. """
            if a > b:
                raise RuntimeError

        wrapped = rika.wrap_no_error(greater)
        self.assertRaises(rika.NoError, wrapped, 1, 2)

    def test_no_error_not_raised_with_two_arguments(self):
        """ test NoError is not raised. function has 2 arguments. """
        def greater(a, b):
            """ function, which has 2 arguments and may raise ValueError. """
            if a > b:
                raise RuntimeError

        wrapped = rika.wrap_no_error(greater)
        self.assertRaises(RuntimeError, wrapped, 2, 1)


class TestPrintHack(unittest.TestCase):
    """ test PrintHack-class."""
    def test_normal1(self):
        """ test normal case. PrintHack.get() is called after with-scope. """
        with rika.PrintHack() as hack:
            print('abc')
            print('edf')
        self.assertEqual(hack.get(), 'abc\nedf\n')

    def test_normal2(self):
        """ test normal case. PrintHack.get() is called in with-scope. """
        with rika.PrintHack() as hack:
            print('abc')
            print('edf')
            self.assertEqual(hack.get(), 'abc\nedf\n')

    def test_reset(self):
        """ test reset function. """
        with rika.PrintHack() as hack:
            print('abc')
            hack.reset()
            print('edf')
        self.assertEqual(hack.get(), 'edf\n')

    def test_without_with(self):
        """ test with-statement is not used. """
        hack = rika.PrintHack()
        print('abc')
        self.assertEqual(hack.get(), '')

    def test_duplex(self):
        """ test double with-statement. """
        with rika.PrintHack() as hack1:
            print('abc')
            with rika.PrintHack() as hack2:
                print('edf')
            self.assertEqual(hack2.get(), 'edf\n')
        self.assertEqual(hack1.get(), 'abc\n')


class TestArgvHack(unittest.TestCase):
    """ test argv_hack function."""
    def test_type_error(self):
        """ test TypeError is raised when argument is not list. """
        def inner(argv):
            with rika.argv_hack():
                pass
        self.assertRaises(TypeError, inner, 1)

    def test_works(self):
        """ test argv_hack() works. """
        import sys

        org_sys_argv = sys.argv[::]
        test_argv = ['sample', '--help']

        with rika.argv_hack(test_argv):
            self.assertEqual(test_argv, sys.argv)
        self.assertEqual(org_sys_argv, sys.argv)

    def test_init_takes_no_effect(self):
        """ test argv_hack() takes no effect when in not with statement. """
        import sys

        org_sys_argv = sys.argv[::]
        test_argv = ['sample', '--help']

        rika.argv_hack(test_argv)
        self.assertEqual(org_sys_argv, sys.argv)


class TestScopedFile(unittest.TestCase):
    """ test ScopedFile-class."""
    def test_create_tmpfile(self):
        """ test that tmp file is created. """
        with rika.ScopedFile() as file:
            self.assertTrue(os.path.isfile(file.path))

    def test_remove_tmpfile(self):
        """ test that tmp file is removed after with-statement. """
        with rika.ScopedFile() as file:
            path = file.path
        self.assertFalse(os.path.isfile(path))

    def test_wrong_argument(self):
        """ wrong argument to __init__() should raise TypeError. """
        self.assertRaises(TypeError, rika.ScopedFile, 1, '')
        self.assertRaises(TypeError, rika.ScopedFile, '', 1)

    def test_suffix_argument(self):
        """ test suffix works. """
        with rika.ScopedFile(suffix='.txt') as file:
            self.assertTrue(file.path.endswith('.txt'))

    def test_prefix_argument(self):
        """ test prefix works. """
        with rika.ScopedFile(prefix='txt') as file:
            self.assertTrue(os.path.basename(file.path).startswith('txt'))

    def test_oserror_from_mkstemp(self):
        """ test tempfile.mkstemp() fails because of wrong character. """
        # Watch out! Its result may change according to OS environment
        file = rika.ScopedFile(prefix='slash/')
        self.assertRaises(OSError, file.__enter__)

    def test_read_and_write_works(self):
        """ read() and write() workds. """
        with rika.ScopedFile() as file:
            file.write('123')
            read = file.read()
        self.assertEqual('123', read)

        with rika.ScopedFile() as file:
            file.write(b'123', True)
            read = file.read(True)
        self.assertEqual(b'123', read)

    def test_illegal_timing_read(self):
        """ read() out of with-statement should raise RuntimeError. """
        file = rika.ScopedFile()
        self.assertRaises(RuntimeError, file.read)

        with rika.ScopedFile() as file:
            pass
        self.assertRaises(RuntimeError, file.read)

    def test_illegal_timing_write(self):
        """ write() out of with-statement should raise RuntimeError. """
        file = rika.ScopedFile()
        self.assertRaises(RuntimeError, file.write, '0')

        with rika.ScopedFile() as file:
            pass
        self.assertRaises(RuntimeError, file.write, '0')

    def test_oserror_from_read(self):
        """ read() raises OSError in unexpected situation. """
        import os

        file = rika.ScopedFile()
        file.__enter__()
        os.close(file._ScopedFile__fh)
        os.remove(file.path)
        self.assertRaises(OSError, file.read)

    def test_oserror_from_write(self):
        """ write() raises OSError because argument is wrong. """
        with rika.ScopedFile() as file:
            self.assertRaises(TypeError, file.write, '0', True)

        with rika.ScopedFile() as file:
            self.assertRaises(TypeError, file.write, b'0', False)

if __name__ == '__main__':
    unittest.main()
