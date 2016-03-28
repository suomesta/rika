# -*- coding:utf-8 -*-
""" Utility functions involving hash-sum.

Defines functions, which calculate hash or sum.
adler32, crc32, md5, sha1, sha224, sha256, sha384, and sha512 are supported.
All functions have same arguments type and returns type.
"""

import zlib
import hashlib
import rika

__author__ = 'T.Oda FEC'
__version__ = '1.0.0'


class _WrapZlib(object):
    """ Wrapper class for zlib sum.

    zlib's sum functions for adler32 and crc32 do not have same interface
    with hashlib's hash functions.
    This class wraps sum functions and make it same interface with hashlib's
    hash functions.
    """
    def __init__(self, name):
        """ initialize.

        param[in]  name: shall be 'adler32' or 'crc32'. this value is a key
                         for factory.
        note       self.name and self.digest_size are intentionaly public,
                   in order to have same interface with hashlib. Users can
                   access directly to self.name and self.digest_size
        """
        if name == 'adler32':
            self.name = name
            self.digest_size = 4
            self.__update = zlib.adler32
            self.__data = 1
        elif name == 'crc32':
            self.name = name
            self.digest_size = 4
            self.__update = zlib.crc32
            self.__data = 0
        else:
            # never pass here
            LookupError('unknown sum type: ' + name)

    def update(self, byte_data):
        """ update data

        This method is correspond to update() of hashlib.
        param[in]  byte_data: input byte data.
        """
        self.__data = self.__update(byte_data, self.__data) & 0xffffffff

    def digest(self):
        """ get data in bytes

        This method is correspond to digest() of hashlib.
        return     bytes of data
        """
        return self.__data.to_bytes(self.digest_size, byteorder='big')


def _skeleton(path_or_bytes, block_size, instance):
    """ execute

    calculate hash or sum using instance of class.
    param[in]  path_or_bytes: appointed file path or byte buffer data.
    param[in]  block_size: buffer size of file.read(). shall be int.
                           if path_or_bytes is byte buffer, then ignored.
    param[in]  instance: instance of calculating class. should be _WrapZlib
                         or hashlib's object.
    return     tuple(value, size). [0] is hash or sum value in int, [1] is
               size of value in bytes.
    raise      OSError: an error involving open() or file.read()
               TypeError: path_or_bytes is neither str nor byte buffer, or
                          block_size is not int
    """
    rika.check_type('path_or_bytes', locals(), allow=(str, bytes, bytearray))

    if isinstance(path_or_bytes, str):  # file path
        # check and define block_size
        rika.check_type('block_size', locals(), allow=int)
        block_size = max(1, block_size)

        # create hash or sum from file
        with open(path_or_bytes, 'rb') as file:
            block = file.read(block_size)
            while block:
                instance.update(block)
                block = file.read(block_size)
    else:  # byte buffer
        # create hash or sum from byte buffer
        instance.update(path_or_bytes)

    return (int.from_bytes(instance.digest(), byteorder='big'),
            instance.digest_size)


def adler32(path_or_bytes, block_size=1024):
    """ Adler-32

    Calculate Adler-32 and return Adler-32 value.
    It is a good way to print Adler-32 value is in '08X' format.
    param[in]  path_or_bytes: appointed file path or byte data.
    param[in]  block_size: buffer size of file.read(). shall be int.
                           if path_or_bytes is byte buffer, then ignored.
    note       the argument path_or_bytes is allowed both str or bytes.
               the execution is switched if the path_or_bytes is str or not.
    return     tuple(value, size). [0] is Adler-32 value in int, [1] is size
               of value in bytes (=always 4).
    raise      OSError: an error involving open() or file.read()
               TypeError: path_or_bytes is neither str nor byte buffer, or
                          block_size is not int
    """
    return _skeleton(path_or_bytes, block_size, _WrapZlib('adler32'))


def crc32(path_or_bytes, block_size=1024):
    """ CRC32

    Calculate CRC32 and return CRC32 value.
    It is a good way to print CRC32 value is in '08X' format.
    param[in]  path_or_bytes: appointed file path or byte data.
    param[in]  block_size: buffer size of file.read(). shall be int.
                           if path_or_bytes is byte buffer, then ignored.
    note       the argument path_or_bytes is allowed both str or bytes.
               the execution is switched if the path_or_bytes is str or not.
    return     tuple(value, size). [0] is CRC32 value in int, [1] is size
               of value in bytes (=always 4).
    raise      OSError: an error involving open() or file.read()
               TypeError: path_or_bytes is neither str nor byte buffer, or
                          block_size is not int
    """
    return _skeleton(path_or_bytes, block_size, _WrapZlib('crc32'))


def md5(path_or_bytes, block_size=1024):
    """ MD5

    Calculate MD5 and return MD5 value.
    It is a good way to print MD5 value is in '032X' format.
    param[in]  path_or_bytes: appointed file path or byte data.
    param[in]  block_size: buffer size of file.read(). shall be int.
                           if path_or_bytes is byte buffer, then ignored.
    note       the argument path_or_bytes is allowed both str or bytes.
               the execution is switched if the path_or_bytes is str or not.
    return     tuple(value, size). [0] is MD5 value in int, [1] is size
               of value in bytes (=always 16).
    raise      OSError: an error involving open() or file.read()
               TypeError: path_or_bytes is neither str nor byte buffer, or
                          block_size is not int
    """
    return _skeleton(path_or_bytes, block_size, hashlib.md5())


def sha1(path_or_bytes, block_size=1024):
    """ SHA-1

    Calculate SHA-1 and return SHA-1 value.
    It is a good way to print SHA-1 value is in '040X' format.
    param[in]  path_or_bytes: appointed file path or byte data.
    param[in]  block_size: buffer size of file.read(). shall be int.
                           if path_or_bytes is byte buffer, then ignored.
    note       the argument path_or_bytes is allowed both str or bytes.
               the execution is switched if the path_or_bytes is str or not.
    return     tuple(value, size). [0] is SHA-1 value in int, [1] is size
               of value in bytes (=always 20).
    raise      OSError: an error involving open() or file.read()
               TypeError: path_or_bytes is neither str nor byte buffer, or
                          block_size is not int
    """
    return _skeleton(path_or_bytes, block_size, hashlib.sha1())


def sha224(path_or_bytes, block_size=1024):
    """ SHA-224

    Calculate SHA-224 and return SHA-224 value.
    It is a good way to print SHA-224 value is in '056X' format.
    param[in]  path_or_bytes: appointed file path or byte data.
    param[in]  block_size: buffer size of file.read(). shall be int.
                           if path_or_bytes is byte buffer, then ignored.
    note       the argument path_or_bytes is allowed both str or bytes.
               the execution is switched if the path_or_bytes is str or not.
    return     tuple(value, size). [0] is SHA-224 value in int, [1] is size
               of value in bytes (=always 28).
    raise      OSError: an error involving open() or file.read()
               TypeError: path_or_bytes is neither str nor byte buffer, or
                          block_size is not int
    """
    return _skeleton(path_or_bytes, block_size, hashlib.sha224())


def sha256(path_or_bytes, block_size=1024):
    """ SHA-256

    Calculate SHA-256 and return SHA-224 value.
    It is a good way to print SHA-256 value is in '064X' format.
    param[in]  path_or_bytes: appointed file path or byte data.
    param[in]  block_size: buffer size of file.read(). shall be int.
                           if path_or_bytes is byte buffer, then ignored.
    note       the argument path_or_bytes is allowed both str or bytes.
               the execution is switched if the path_or_bytes is str or not.
    return     tuple(value, size). [0] is SHA-256 value in int, [1] is size
               of value in bytes (=always 32).
    raise      OSError: an error involving open() or file.read()
               TypeError: path_or_bytes is neither str nor byte buffer, or
                          block_size is not int
    """
    return _skeleton(path_or_bytes, block_size, hashlib.sha256())


def sha384(path_or_bytes, block_size=1024):
    """ SHA-384

    Calculate SHA-384 and return SHA-384 value.
    It is a good way to print SHA-384 value is in '096X' format.
    param[in]  path_or_bytes: appointed file path or byte data.
    param[in]  block_size: buffer size of file.read(). shall be int.
                           if path_or_bytes is byte buffer, then ignored.
    note       the argument path_or_bytes is allowed both str or bytes.
               the execution is switched if the path_or_bytes is str or not.
    return     tuple(value, size). [0] is SHA-384 value in int, [1] is size
               of value in bytes (=always 48).
    raise      OSError: an error involving open() or file.read()
               TypeError: path_or_bytes is neither str nor byte buffer, or
                          block_size is not int
    """
    return _skeleton(path_or_bytes, block_size, hashlib.sha384())


def sha512(path_or_bytes, block_size=1024):
    """ SHA-512

    Calculate SHA-512 and return SHA-512 value.
    It is a good way to print SHA-512 value is in '0128X' format.
    param[in]  path_or_bytes: appointed file path or byte data.
    param[in]  block_size: buffer size of file.read(). shall be int.
                           if path_or_bytes is byte buffer, then ignored.
    note       the argument path_or_bytes is allowed both str or bytes.
               the execution is switched if the path_or_bytes is str or not.
    return     tuple(value, size). [0] is SHA-512 value in int, [1] is size
               of value in bytes (=always 64).
    raise      OSError: an error involving open() or file.read()
               TypeError: path_or_bytes is neither str nor byte buffer, or
                          block_size is not int
    """
    return _skeleton(path_or_bytes, block_size, hashlib.sha512())
