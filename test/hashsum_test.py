# -*- coding:utf-8 -*-
""" unit test of hashsum.

Here testing adler32(), crc32(), md5(), sha1(), sha224(), sha256(), sha384(),
and sha512() in rika.hashsum.py

All functions are tested by one class.
Two files are stored to ./data/hashsum folder.
Main procedure is to calculate hashsum of these files.
Required result is calculated by Windows free software 'HashSum'.
"""

import unittest
import os.path
import sys
_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(_SCRIPT_DIR, '..', '..'))
import rika.hashsum

__author__ = 'suomesta'
__version__ = '1.0.0'

_PNG = os.path.join('data', 'hashsum', 'python-logo-master-v3-TM.png')
_EMPTY = os.path.join('data', 'hashsum', 'empty')
_NOT_FOUND = os.path.join('data', 'hashsum', 'notfound')


def _to_str(result):
    """ convert from the result of hashsum function into str

    param[in]  result: return value of hashsum function. This should be tuple.
    return     created str in hex lower case
    """
    return ('{0:0' + str(result[1] * 2) + 'x}').format(result[0])


class TestAdler32(unittest.TestCase):
    """ test adler32(). """
    def test_png_file_name(self):
        """ test adler32() using file name to png. """
        self.assertEqual(
            '6191cfb5',
            _to_str(rika.hashsum.adler32(_PNG))
        )
        self.assertEqual(
            '6191cfb5',
            _to_str(rika.hashsum.adler32(_PNG, 1))
        )
        self.assertEqual(
            '6191cfb5',
            _to_str(rika.hashsum.adler32(_PNG, 0))
        )

    def test_png_binary(self):
        """ test adler32() using binary to png. """
        with open(_PNG, 'rb') as file:
            b = file.read()
        self.assertEqual(
            '6191cfb5',
            _to_str(rika.hashsum.adler32(b))
        )

    def test_empty_file_name(self):
        """ test adler32() using file name to empty. """
        self.assertEqual(
            '00000001',
            _to_str(rika.hashsum.adler32(_EMPTY))
        )
        self.assertEqual(
            '00000001',
            _to_str(rika.hashsum.adler32(_EMPTY, 1))
        )
        self.assertEqual(
            '00000001',
            _to_str(rika.hashsum.adler32(_EMPTY, 0))
        )

    def test_empty_binary(self):
        """ test adler32() using binary to empty. """
        with open(_EMPTY, 'rb') as file:
            b = file.read()
        self.assertEqual(
            '00000001',
            _to_str(rika.hashsum.adler32(b))
        )

    def test_not_found(self):
        """ test adler32() using file name to not found. """
        self.assertRaises(
            (OSError, TypeError, ValueError),
            rika.hashsum.adler32, _NOT_FOUND
        )

    def test_wrong_path_or_bytes(self):
        """ test adler32() using wrong path_or_bytes. """
        self.assertRaises(
            TypeError,
            rika.hashsum.adler32, 1, 1024
        )

    def test_wrong_block_size(self):
        """ test adler32() using wrong block_size. """
        self.assertRaises(
            TypeError,
            rika.hashsum.adler32, _EMPTY, 1.0
        )


class TestCrc32(unittest.TestCase):
    """ test crc32(). """
    def test_png_file_name(self):
        """ test crc32() using file name to png. """
        self.assertEqual(
            'd5db66c6',
            _to_str(rika.hashsum.crc32(_PNG))
        )
        self.assertEqual(
            'd5db66c6',
            _to_str(rika.hashsum.crc32(_PNG, 1))
        )
        self.assertEqual(
            'd5db66c6',
            _to_str(rika.hashsum.crc32(_PNG, 0))
        )

    def test_png_binary(self):
        """ test crc32() using binary to png. """
        with open(_PNG, 'rb') as file:
            b = file.read()
        self.assertEqual(
            'd5db66c6',
            _to_str(rika.hashsum.crc32(b))
        )

    def test_empty_file_name(self):
        """ test crc32() using file name to empty. """
        self.assertEqual(
            '00000000',
            _to_str(rika.hashsum.crc32(_EMPTY))
        )
        self.assertEqual(
            '00000000',
            _to_str(rika.hashsum.crc32(_EMPTY, 1))
        )
        self.assertEqual(
            '00000000',
            _to_str(rika.hashsum.crc32(_EMPTY, 0))
        )

    def test_empty_binary(self):
        """ test crc32() using binary to empty. """
        with open(_EMPTY, 'rb') as file:
            b = file.read()
        self.assertEqual(
            '00000000',
            _to_str(rika.hashsum.crc32(b))
        )

    def test_not_found(self):
        """ test crc32() using file name to not found. """
        self.assertRaises(
            (OSError, TypeError, ValueError),
            rika.hashsum.crc32, _NOT_FOUND
        )

    def test_wrong_path_or_bytes(self):
        """ test crc32() using wrong path_or_bytes. """
        self.assertRaises(
            TypeError,
            rika.hashsum.crc32, 1, 1024
        )

    def test_wrong_block_size(self):
        """ test crc32() using wrong block_size. """
        self.assertRaises(
            TypeError,
            rika.hashsum.crc32, _EMPTY, 1.0
        )


class TestMd5(unittest.TestCase):
    """ test md5(). """
    def test_png_file_name(self):
        """ test md5() using file name to png. """
        self.assertEqual(
            '3cf229eedc092549277e8859aad2fca5',
            _to_str(rika.hashsum.md5(_PNG))
        )
        self.assertEqual(
            '3cf229eedc092549277e8859aad2fca5',
            _to_str(rika.hashsum.md5(_PNG, 1))
        )
        self.assertEqual(
            '3cf229eedc092549277e8859aad2fca5',
            _to_str(rika.hashsum.md5(_PNG, 0))
        )

    def test_png_binary(self):
        """ test md5() using binary to png. """
        with open(_PNG, 'rb') as file:
            b = file.read()
        self.assertEqual(
            '3cf229eedc092549277e8859aad2fca5',
            _to_str(rika.hashsum.md5(b))
        )

    def test_empty_file_name(self):
        """ test md5() using file name to empty. """
        self.assertEqual(
            'd41d8cd98f00b204e9800998ecf8427e',
            _to_str(rika.hashsum.md5(_EMPTY))
        )
        self.assertEqual(
            'd41d8cd98f00b204e9800998ecf8427e',
            _to_str(rika.hashsum.md5(_EMPTY, 1))
        )
        self.assertEqual(
            'd41d8cd98f00b204e9800998ecf8427e',
            _to_str(rika.hashsum.md5(_EMPTY, 0))
        )

    def test_empty_binary(self):
        """ test md5() using binary to empty. """
        with open(_EMPTY, 'rb') as file:
            b = file.read()
        self.assertEqual(
            'd41d8cd98f00b204e9800998ecf8427e',
            _to_str(rika.hashsum.md5(b))
        )

    def test_not_found(self):
        """ test md5() using file name to not found. """
        self.assertRaises(
            (OSError, TypeError, ValueError),
            rika.hashsum.md5, _NOT_FOUND
        )

    def test_wrong_path_or_bytes(self):
        """ test md5() using wrong path_or_bytes. """
        self.assertRaises(
            TypeError,
            rika.hashsum.md5, 1, 1024
        )

    def test_wrong_block_size(self):
        """ test md5() using wrong block_size. """
        self.assertRaises(
            TypeError,
            rika.hashsum.md5, _EMPTY, 1.0
        )


class TestSha1(unittest.TestCase):
    """ test sha1(). """
    def test_png_file_name(self):
        """ test sha1() using file name to png. """
        self.assertEqual(
            'c8a756475599e6e3c904b24077b4b0a31983752c',
            _to_str(rika.hashsum.sha1(_PNG))
        )
        self.assertEqual(
            'c8a756475599e6e3c904b24077b4b0a31983752c',
            _to_str(rika.hashsum.sha1(_PNG, 1))
        )
        self.assertEqual(
            'c8a756475599e6e3c904b24077b4b0a31983752c',
            _to_str(rika.hashsum.sha1(_PNG, 0))
        )

    def test_png_binary(self):
        """ test sha1() using binary to png. """
        with open(_PNG, 'rb') as file:
            b = file.read()
        self.assertEqual(
            'c8a756475599e6e3c904b24077b4b0a31983752c',
            _to_str(rika.hashsum.sha1(b))
        )

    def test_empty_file_name(self):
        """ test sha1() using file name to empty. """
        self.assertEqual(
            'da39a3ee5e6b4b0d3255bfef95601890afd80709',
            _to_str(rika.hashsum.sha1(_EMPTY))
        )
        self.assertEqual(
            'da39a3ee5e6b4b0d3255bfef95601890afd80709',
            _to_str(rika.hashsum.sha1(_EMPTY, 1))
        )
        self.assertEqual(
            'da39a3ee5e6b4b0d3255bfef95601890afd80709',
            _to_str(rika.hashsum.sha1(_EMPTY, 0))
        )

    def test_empty_binary(self):
        """ test sha1() using binary to empty. """
        with open(_EMPTY, 'rb') as file:
            b = file.read()
        self.assertEqual(
            'da39a3ee5e6b4b0d3255bfef95601890afd80709',
            _to_str(rika.hashsum.sha1(b))
        )

    def test_not_found(self):
        """ test sha1() using file name to not found. """
        self.assertRaises(
            (OSError, TypeError, ValueError),
            rika.hashsum.sha1, _NOT_FOUND
        )

    def test_wrong_path_or_bytes(self):
        """ test sha1() using wrong path_or_bytes. """
        self.assertRaises(
            TypeError,
            rika.hashsum.sha1, 1, 1024
        )

    def test_wrong_block_size(self):
        """ test sha1() using wrong block_size. """
        self.assertRaises(
            TypeError,
            rika.hashsum.sha1, _EMPTY, 1.0
        )


class TestSha224(unittest.TestCase):
    """ test sha224(). """
    def test_png_file_name(self):
        """ test sha224() using file name to png. """
        self.assertEqual(
            'e4b8d67cc135a51a43678130b9a6fb8372854fbc4458a96aa6f35f0c',
            _to_str(rika.hashsum.sha224(_PNG))
        )
        self.assertEqual(
            'e4b8d67cc135a51a43678130b9a6fb8372854fbc4458a96aa6f35f0c',
            _to_str(rika.hashsum.sha224(_PNG, 1))
        )
        self.assertEqual(
            'e4b8d67cc135a51a43678130b9a6fb8372854fbc4458a96aa6f35f0c',
            _to_str(rika.hashsum.sha224(_PNG, 0))
        )

    def test_png_binary(self):
        """ test sha224() using binary to png. """
        with open(_PNG, 'rb') as file:
            b = file.read()
        self.assertEqual(
            'e4b8d67cc135a51a43678130b9a6fb8372854fbc4458a96aa6f35f0c',
            _to_str(rika.hashsum.sha224(b))
        )

    def test_empty_file_name(self):
        """ test sha224() using file name to empty. """
        self.assertEqual(
            'd14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f',
            _to_str(rika.hashsum.sha224(_EMPTY))
        )
        self.assertEqual(
            'd14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f',
            _to_str(rika.hashsum.sha224(_EMPTY, 1))
        )
        self.assertEqual(
            'd14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f',
            _to_str(rika.hashsum.sha224(_EMPTY, 0))
        )

    def test_empty_binary(self):
        """ test sha224() using binary to empty. """
        with open(_EMPTY, 'rb') as file:
            b = file.read()
        self.assertEqual(
            'd14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f',
            _to_str(rika.hashsum.sha224(b))
        )

    def test_not_found(self):
        """ test sha224() using file name to not found. """
        self.assertRaises(
            (OSError, TypeError, ValueError),
            rika.hashsum.sha224, _NOT_FOUND
        )

    def test_wrong_path_or_bytes(self):
        """ test sha224() using wrong path_or_bytes. """
        self.assertRaises(
            TypeError,
            rika.hashsum.sha224, 1, 1024
        )

    def test_wrong_block_size(self):
        """ test sha224() using wrong block_size. """
        self.assertRaises(
            TypeError,
            rika.hashsum.sha224, _EMPTY, 1.0
        )


class TestSha256(unittest.TestCase):
    """ test sha256(). """
    def test_png_file_name(self):
        """ test sha256() using file name to png. """
        self.assertEqual(
            '515d56e5b2bb0ea82350bc42fca54149ca135815a1c7d3fedd8e44615a77d37a',
            _to_str(rika.hashsum.sha256(_PNG))
        )
        self.assertEqual(
            '515d56e5b2bb0ea82350bc42fca54149ca135815a1c7d3fedd8e44615a77d37a',
            _to_str(rika.hashsum.sha256(_PNG, 1))
        )
        self.assertEqual(
            '515d56e5b2bb0ea82350bc42fca54149ca135815a1c7d3fedd8e44615a77d37a',
            _to_str(rika.hashsum.sha256(_PNG, 0))
        )

    def test_png_binary(self):
        """ test sha256() using binary to png. """
        with open(_PNG, 'rb') as file:
            b = file.read()
        self.assertEqual(
            '515d56e5b2bb0ea82350bc42fca54149ca135815a1c7d3fedd8e44615a77d37a',
            _to_str(rika.hashsum.sha256(b))
        )

    def test_empty_file_name(self):
        """ test sha256() using file name to empty. """
        self.assertEqual(
            'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            _to_str(rika.hashsum.sha256(_EMPTY))
        )
        self.assertEqual(
            'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            _to_str(rika.hashsum.sha256(_EMPTY, 1))
        )
        self.assertEqual(
            'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            _to_str(rika.hashsum.sha256(_EMPTY, 0))
        )

    def test_empty_binary(self):
        """ test sha256() using binary to empty. """
        with open(_EMPTY, 'rb') as file:
            b = file.read()
        self.assertEqual(
            'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            _to_str(rika.hashsum.sha256(b))
        )

    def test_not_found(self):
        """ test sha256() using file name to not found. """
        self.assertRaises(
            (OSError, TypeError, ValueError),
            rika.hashsum.sha256, _NOT_FOUND
        )

    def test_wrong_path_or_bytes(self):
        """ test sha256() using wrong path_or_bytes. """
        self.assertRaises(
            TypeError,
            rika.hashsum.sha256, 1, 1024
        )

    def test_wrong_block_size(self):
        """ test sha256() using wrong block_size. """
        self.assertRaises(
            TypeError,
            rika.hashsum.sha256, _EMPTY, 1.0
        )


class TestSha384(unittest.TestCase):
    """ test sha384(). """
    def test_png_file_name(self):
        """ test sha384() using file name to png. """
        self.assertEqual(
            'e750a21f80cf6ac575c35112b26dbc6c54003c13c4de14f85e39c9f788acd09150b128ebc5abff3452e13f8cfc319ef2',
            _to_str(rika.hashsum.sha384(_PNG))
        )
        self.assertEqual(
            'e750a21f80cf6ac575c35112b26dbc6c54003c13c4de14f85e39c9f788acd09150b128ebc5abff3452e13f8cfc319ef2',
            _to_str(rika.hashsum.sha384(_PNG, 1))
        )
        self.assertEqual(
            'e750a21f80cf6ac575c35112b26dbc6c54003c13c4de14f85e39c9f788acd09150b128ebc5abff3452e13f8cfc319ef2',
            _to_str(rika.hashsum.sha384(_PNG, 0))
        )

    def test_png_binary(self):
        """ test sha384() using binary to png. """
        with open(_PNG, 'rb') as file:
            b = file.read()
        self.assertEqual(
            'e750a21f80cf6ac575c35112b26dbc6c54003c13c4de14f85e39c9f788acd09150b128ebc5abff3452e13f8cfc319ef2',
            _to_str(rika.hashsum.sha384(b))
        )

    def test_empty_file_name(self):
        """ test sha384() using file name to empty. """
        self.assertEqual(
            '38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95b',
            _to_str(rika.hashsum.sha384(_EMPTY))
        )
        self.assertEqual(
            '38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95b',
            _to_str(rika.hashsum.sha384(_EMPTY, 1))
        )
        self.assertEqual(
            '38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95b',
            _to_str(rika.hashsum.sha384(_EMPTY, 0))
        )

    def test_empty_binary(self):
        """ test sha384() using binary to empty. """
        with open(_EMPTY, 'rb') as file:
            b = file.read()
        self.assertEqual(
            '38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95b',
            _to_str(rika.hashsum.sha384(b))
        )

    def test_not_found(self):
        """ test sha384() using file name to not found. """
        self.assertRaises(
            (OSError, TypeError, ValueError),
            rika.hashsum.sha384, _NOT_FOUND
        )

    def test_wrong_path_or_bytes(self):
        """ test sha384() using wrong path_or_bytes. """
        self.assertRaises(
            TypeError,
            rika.hashsum.sha384, 1, 1024
        )

    def test_wrong_block_size(self):
        """ test sha384() using wrong block_size. """
        self.assertRaises(
            TypeError,
            rika.hashsum.sha384, _EMPTY, 1.0
        )


class TestSha512(unittest.TestCase):
    """ test sha512(). """
    def test_png_file_name(self):
        """ test sha512() using file name to png. """
        self.assertEqual(
            '21f670641653b2c80d28226a498ed9d27466691767a9ebde64fb982bc8afc6b21750a990bfc2a49340173c6a2a70a8fe59dd41e9dc62ada440f9205bb59a6422',
            _to_str(rika.hashsum.sha512(_PNG))
        )
        self.assertEqual(
            '21f670641653b2c80d28226a498ed9d27466691767a9ebde64fb982bc8afc6b21750a990bfc2a49340173c6a2a70a8fe59dd41e9dc62ada440f9205bb59a6422',
            _to_str(rika.hashsum.sha512(_PNG, 1))
        )
        self.assertEqual(
            '21f670641653b2c80d28226a498ed9d27466691767a9ebde64fb982bc8afc6b21750a990bfc2a49340173c6a2a70a8fe59dd41e9dc62ada440f9205bb59a6422',
            _to_str(rika.hashsum.sha512(_PNG, 0))
        )

    def test_png_binary(self):
        """ test sha512() using binary to png. """
        with open(_PNG, 'rb') as file:
            b = file.read()
        self.assertEqual(
            '21f670641653b2c80d28226a498ed9d27466691767a9ebde64fb982bc8afc6b21750a990bfc2a49340173c6a2a70a8fe59dd41e9dc62ada440f9205bb59a6422',
            _to_str(rika.hashsum.sha512(b))
        )

    def test_empty_file_name(self):
        """ test sha512() using file name to empty. """
        self.assertEqual(
            'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e',
            _to_str(rika.hashsum.sha512(_EMPTY))
        )
        self.assertEqual(
            'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e',
            _to_str(rika.hashsum.sha512(_EMPTY, 1))
        )
        self.assertEqual(
            'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e',
            _to_str(rika.hashsum.sha512(_EMPTY, 0))
        )

    def test_empty_binary(self):
        """ test sha512() using binary to empty. """
        with open(_EMPTY, 'rb') as file:
            b = file.read()
        self.assertEqual(
            'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e',
            _to_str(rika.hashsum.sha512(b))
        )

    def test_not_found(self):
        """ test sha512() using file name to not found. """
        self.assertRaises(
            (OSError, TypeError, ValueError),
            rika.hashsum.sha512, _NOT_FOUND
        )

    def test_wrong_path_or_bytes(self):
        """ test sha512() using wrong path_or_bytes. """
        self.assertRaises(
            TypeError,
            rika.hashsum.sha512, 1, 1024
        )

    def test_wrong_block_size(self):
        """ test sha512() using wrong block_size. """
        self.assertRaises(
            TypeError,
            rika.hashsum.sha512, _EMPTY, 1.0
        )

if __name__ == '__main__':
    unittest.main()
