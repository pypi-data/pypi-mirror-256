#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import time
import re
import subprocess


class StreamVerifier:
    '''
    @brief A verifier class which checks stream.
    '''


    def __init__(self, stream):
        '''
        @brief Constructor.
        @param[in] stream The stream which have following intergaces interface.
                   readline(), close(), closed.
        '''
        self.__stream = stream

        # sanity check
        if hasattr(stream, 'readline') and callable(stream.readline):
            self.__stream = stream
        else:
            raise TypeError('The specified stream object does not have {0}.'.format('readline() method'))

        if hasattr(stream, 'close') and callable(stream.close):
            self.__stream = stream
        else:
            raise TypeError('The specified stream object does not have {0}.'.format('close() method'))

        if hasattr(stream, 'closed'):
            self.__stream = stream
        else:
            raise TypeError('The specified stream object does not have {0}.'.format('closed attribute'))


    def __del__(self):
        if self.__stream.closed:
            pass
        else:
            self.__stream.close()


    def assertPattern(self, pattern, timeout = 30):
        '''
        @brief Verifies specified pattern in this stream in specified toumeout.
        @param[in] pattern The pattern.
        @param[in] timeout The timeout duration. The unit is secounds.
        '''

        # sanity check
        assert timeout >= 0, 'timeout expected greater or equal to zero. But actual is {0}.'.format(timeout)

        # variables for timeout detection
        schedule_timeout = time.time() + timeout

        # Memorize first line for exception message
        first_line = None

        while True:
            time_current = time.time()

            # read stream
            line = self.__stream.readline().rstrip()
            if first_line is None:
                first_line = line

            # expected condition?
            if re.search(pattern, line):
                # exit from this assertion.
                break
            else:
                # continue to seek stream
                pass

            # timeout?
            if time_current >= schedule_timeout:
                raise AssertionError(
                    'Expected pattern "{0}" is not found.\nFrom "{1}" in {2} seconds'.format(pattern, first_line, timeout)
                    )
            else:
                if len(line) > 0:
                    # continue to seek stream without wait
                    pass
                else:
                    # Empty line. Assumed EOL.
                    time.sleep(0.1)


    def seekMostRecent(self):
        while True:
            line = self.__stream.readline().rstrip()

            if len(line) > 0:
                pass
            else:
                # Empty line. Assumed EOL.
                break;


if __name__ == '__main__':
    # executed
    pass
else:
    # imported
    pass
