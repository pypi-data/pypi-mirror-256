#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import time


def assertFileExist(path, timeout = 0):
    '''
    @brief Verifies that a file specified with path exists.
    '''

    # sanity check
    assert timeout >= 0, 'timeout expected greater or equal to zero. But actual is {0}.'.format(timeout)

    schedule_timeout = time.time() + timeout

    while True:
        time_current = time.time()

        # expected condition?
        if os.path.isfile(path):
            break

        # timeout?
        if time_current > schedule_timeout:
            raise AssertionError(
                'File "{0}" expected to exist. But does not be created for {0} secounds.'.format(path, timeout)
                )
        else:
            time.sleep(0.1)


def assertFileNotExist(path, timeout = 0):
    '''
    @brief Verifies that a file specified with path does not exist.
    '''

    # sanity check
    assert timeout >= 0, 'timeout expected greater or equal to zero. But actual is {0}.'.format(timeout)

    schedule_timeout = time.time() + timeout

    while True:
        time_current = time.time()

        # expected condition?
        if not os.path.isfile(path):
            break

        # timeout?
        if time_current > schedule_timeout:
            raise AssertionError(
                'File "{0}" expected NOT to exist. But does not be removed for {0} secounds.'.format(path, timeout)
                )
        else:
            time.sleep(0.1)


def assertDirectoryExist(path, timeout = 0):
    '''
    @brief Verifies that a directory specified with path exists.
    '''

    # sanity check
    assert timeout >= 0, 'timeout expected greater or equal to zero. But actual is {0}.'.format(timeout)

    schedule_timeout = time.time() + timeout

    while True:
        time_current = time.time()

        # expected condition?
        if os.path.isdir(path):
            break

        # timeout?
        if time_current > schedule_timeout:
            raise AssertionError(
                'Directory "{0}" expected to exist. But does not be created for {0} secounds.'.format(path, timeout)
                )
        else:
            time.sleep(0.1)


def assertDirectoryNotExist(path, timeout = 0):
    '''
    @brief Verifies that a directory specified with path does not exist.
    '''

    # sanity check
    assert timeout >= 0, 'timeout expected greater or equal to zero. But actual is {0}.'.format(timeout)

    schedule_timeout = time.time() + timeout

    while True:
        time_current = time.time()

        # expected condition?
        if not os.path.isdir(path):
            break

        # timeout?
        if time_current > schedule_timeout:
            raise AssertionError(
                'Directory "{0}" expected NOT to exist. But does not be removed for {0} secounds.'.format(path, timeout)
                )
        else:
            time.sleep(0.1)


if __name__ == '__main__':
    # executed
    pass
else:
    # imported
    pass
