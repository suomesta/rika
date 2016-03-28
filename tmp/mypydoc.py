# -*- coding:utf-8 -*-
""" pydoc wrapper.

Replace pydoc.visiblename into other one.
New visiblename does output private variables and methods.
The usage is same as pydoc. Typical usage is,
> python mypydoc.py -w target
"""

__author__ = 'T.Oda FEC'
__version__ = '1.0.0'

import pydoc

def my_visiblename(name, all=None, obj=None):
    """Decide whether to show documentation on a variable.

    original is from pydoc version 3.4.
    last line is modified to output protect and private values and methods.
    pylint may point some lines, but no need to mind.
    """
    # Certain special names are redundant or internal.
    # XXX Remove __initializing__?
    if name in ['__author__', '__builtins__', '__cached__', '__credits__',
                '__date__', '__doc__', '__file__', '__spec__',
                '__loader__', '__module__', '__name__', '__package__',
                '__path__', '__qualname__', '__slots__', '__version__']:
        return 0
    # Private names are hidden, but special names are displayed.
    if name.startswith('__') and name.endswith('__'): return 1
    # Namedtuples have public fields and methods with a single leading underscore
    if name.startswith('_') and hasattr(obj, '_fields'):
        return True
    if all is not None:
        # only document that which the programmer exported in __all__
        return name in all
    else:
        # change below line to output protect or private values and methods
        return True
#        return not name.startswith('_')

def main():
    """ main function.

    replace pydoc.visiblename(), and call pydoc.cli().
    pydoc.cli() is regarded as main() of pydoc
    """
    pydoc.visiblename = my_visiblename
    pydoc.cli()

if __name__ == '__main__':
    main()
