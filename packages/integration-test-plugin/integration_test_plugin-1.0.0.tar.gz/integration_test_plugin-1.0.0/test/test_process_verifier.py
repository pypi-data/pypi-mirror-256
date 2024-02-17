#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

import os
import time
import subprocess

import integration_test_plugin.process_verifier as process_verifier


class TestProcessVerifier(unittest.TestCase):


    def setUp(self):
        self.__data_dir = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'data'


    def test_typical_1(self):
        obj = process_verifier.ProcessVerifier(
            subprocess.Popen(
                ('python', '--help'),
                stdout = subprocess.PIPE,
                stderr = subprocess.STDOUT
                ) )

        obj.assertExit(0) # verify exit in timeout(default) and exit code


    def test_typical_2(self):
        obj = process_verifier.ProcessVerifier(
            subprocess.Popen(
                ('python', '--does_not_exist'),
                stdout = subprocess.PIPE,
                stderr = subprocess.STDOUT
                ) )

        obj.assertExit() # verify just exit in timeout(default)


    def test_typical_fail_timeout(self):
        obj = process_verifier.ProcessVerifier(
            subprocess.Popen(
                ('python', '-B', self.__data_dir + os.sep + 'sleep_3_seconds.py'),
                stdout = subprocess.PIPE,
                stderr = subprocess.STDOUT
                ) )

        time_start = time.time()
        with self.assertRaises(AssertionError):
            obj.assertExit(0, timeout = 1)
        time_end = time.time()

        # check the test case does not wait too long
        self.assertTrue( (time_end - time_start) < 10 )


    def test_typical_fail_exit_code(self):
        obj = process_verifier.ProcessVerifier(
            subprocess.Popen(
                ('python', '--does_not_exist'),
                stdout = subprocess.PIPE,
                stderr = subprocess.STDOUT
                ) )

        obj.assertExit(2)


    def test_wrong_argument(self):
        obj = process_verifier.ProcessVerifier(
            subprocess.Popen(
                ('python', '--help'),
                stdout = subprocess.PIPE,
                stderr = subprocess.STDOUT
                ) )

        with self.assertRaises(AssertionError):
            obj.assertExit(0, timeout = -1)


if __name__ == '__main__':
    # executed
    unittest.main()
