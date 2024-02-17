#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import subprocess


class ProcessVerifier():
    '''
    @brief A verifier class which checks stream exit.
    '''


    def __init__(self, process):
        '''
        @brief Constructor.
        @param[in] process The subprocess.Popen instance.
        '''
        self.__command = None
        self.__process = None

        # sanity check
        if isinstance(process, subprocess.Popen):
            self.__process = process
        else:
            raise TypeError('Specified argument process is not subprocess.Popen type')


    def __del__(self):
        if self.__process is None:
            pass # Nothing to do. This process has already terminated.
        else:
            self._closeStreams()
            self.__process.kill()
            self.__process.wait()
            self.__process = None


    def assertExit(self, exit_code = None, timeout = 30):
        '''
        @brief Verifies that this process exits in specified duration and returns specified value.
        @param[in] exit_code The expected exit code. And None means don't care.
        @param[in] timeout The timeout duration.
        @post This process is terminated.
        '''

        # sanity check
        assert timeout >= 0, 'timeout expected greater or equal to zero. But actual is {0}.'.format(timeout)

        try:
            self.__process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired as e:
            # runnning
            self._closeStreams()
            self.__process.kill()
            self.__process.wait()
            self.__process = None
            raise AssertionError('This process does not terminate for {0} seconds'.format(timeout))
        else:
            self._closeStreams()
            if exit_code is None:
                pass # user does not care
            else:
                if self.__process.returncode == exit_code:
                    pass # expected exit code returned
                else:
                    raise AssertionError('Expected exit code is {0} but actually {1}'.format(exit_code, self.__process.returncode))


    def _closeStreams(self):
        # close streams
        if (self.__process.stdin is not None) and (not self.__process.stdin.closed):
            self.__process.stdin.close()

        if (self.__process.stdout is not None) and (not self.__process.stdout.closed):
            self.__process.stdout.close()

        if (self.__process.stderr is not None) and (not self.__process.stderr.closed):
            self.__process.stderr.close()


if __name__ == '__main__':
    # executed
    pass
else:
    # imported
    pass
