#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

import os
import shutil
import tempfile
import logging

import integration_test_plugin.stream_verifier as stream_verifier


class TestStreamVerifier(unittest.TestCase):


    def setUp(self):
        self.__data_dir = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'data'


    def test_typical(self):
        with open(self.__data_dir + os.sep + 'logging_typical.txt', 'r') as fd:
            obj = stream_verifier.StreamVerifier(fd)

            obj.assertPattern(r'Start initialization')
            obj.assertPattern(r'Initialization done')
            obj.assertPattern(r'Start operation')
            obj.assertPattern(r'Shutdown. Wait for power off.')


    def test_timeout_stream(self):
        with open(self.__data_dir + os.sep + 'logging_error.txt', 'r') as fd:
            obj = stream_verifier.StreamVerifier(fd)

            obj.assertPattern(r'Start initialization')

            with self.assertRaises(AssertionError) as cm:
                obj.assertPattern(r'Initialization done', timeout = 1)
            self.assertEqual(
                'Expected pattern "Initialization done" is not found.\nFrom "2024-02-01 10:00:05.000 ERROR   Some parts are broken" in 1 seconds',
                str(cm.exception)
            )


    def test_timeout_crash(self):
        with open(self.__data_dir + os.sep + 'logging_crash.txt', 'r') as fd:
            obj = stream_verifier.StreamVerifier(fd)

            obj.assertPattern(r'Start initialization')

            with self.assertRaises(AssertionError) as cm:
                obj.assertPattern(r'Initialization done', timeout = 1)
            self.assertEqual(
                'Expected pattern "Initialization done" is not found.\nFrom "" in 1 seconds',
                str(cm.exception)
            )


    def test_seek(self):
        with open(self.__data_dir + os.sep + 'logging_typical.txt', 'r') as fd:
            obj = stream_verifier.StreamVerifier(fd)

            obj.seekMostRecent()


    def test_wrong_argument(self):
        with open(self.__data_dir + os.sep + 'logging_typical.txt', 'r') as fd:
            obj = stream_verifier.StreamVerifier(fd)

            with self.assertRaises(AssertionError):
                obj.assertPattern(r'Start initialization', timeout = -1)


if __name__ == '__main__':
    # executed
    unittest.main()
