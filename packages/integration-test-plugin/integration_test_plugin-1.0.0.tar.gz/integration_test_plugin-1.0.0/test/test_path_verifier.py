#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

import os
import shutil
import tempfile
import logging

import integration_test_plugin.path_verifier as path_verifier


class TestPathVerifier(unittest.TestCase):


    def test_assertFileExist(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path_exist = tmpdir + os.sep + 'exist.txt'
            open(path_exist, 'w').close() # create a file

            path_verifier.assertFileExist(path_exist)

            with self.assertRaises(AssertionError):
                path_verifier.assertFileExist(tmpdir + os.sep + 'does_not_exist', timeout = 1)


    def test_assertFileNotExist(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path_exist = tmpdir + os.sep + 'exist.txt'
            open(path_exist, 'w').close() # create a file

            path_verifier.assertFileNotExist(tmpdir + os.sep + 'does_not_exist')

            with self.assertRaises(AssertionError):
                path_verifier.assertFileNotExist(path_exist, timeout = 1)


    def test_assertDirectoryExist(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path_verifier.assertDirectoryExist(tmpdir)

            with self.assertRaises(AssertionError):
                path_verifier.assertDirectoryExist(tmpdir + os.sep + 'does_not_exist', timeout = 1)


    def test_assertDirectoryNotExist(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path_verifier.assertDirectoryNotExist(tmpdir + os.sep + 'does_not_exist')

            with self.assertRaises(AssertionError):
                path_verifier.assertDirectoryNotExist(tmpdir, timeout = 1)


if __name__ == '__main__':
    # executed
    unittest.main()
