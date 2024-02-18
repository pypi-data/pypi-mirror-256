'''Testing cli arguments and actions'''

from pathlib import Path
import unittest
import unittest.mock

from sca2d.__main__ import main


class IgnoreTestCase(unittest.TestCase):
    '''Testing the ignore cli option.'''

    @classmethod
    def setUpClass(cls):
        '''Patch printing methods to suppress output, patch Analyser class to
        assert on calls.
        '''
        cls.patchers = (
            unittest.mock.patch('sca2d.__main__.print'),
            unittest.mock.patch('sca2d.__main__.print_messages'),
            unittest.mock.patch('sca2d.__main__.Analyser', autospec=True),
        )
        mocks = tuple(patcher.start() for patcher in cls.patchers)
        cls.analyser = mocks[-1].return_value
        cls.analyser.analyse_file.return_value = (tuple(), tuple(), )
        cls.test_file = 'tests/scadfiles/lib_foobar.scad'
        cls.test_dir = 'tests/scadfiles'
        cls.test_dir_files = tuple(Path(cls.test_dir).glob('*.scad'))

    @classmethod
    def tearDownClass(cls):
        '''Un-patch'''
        for patcher in cls.patchers:
            patcher.stop()

    def tearDown(self):
        '''Reset analyse_file for each test'''
        self.analyser.analyse_file.reset_mock()

    def test_none_on_file(self):
        '''Tests no ignores passed correctly for single file'''
        main((self.test_file, ))
        self.analyser.analyse_file.assert_called_once_with(self.test_file, output_tree=False, ignore_list=[])

    def test_single_on_file(self):
        '''Tests single ignore is passed for single file'''
        main((self.test_file, '--ignore', 'W1003'))
        self.analyser.analyse_file.assert_called_once_with(self.test_file, output_tree=False, ignore_list=['W1003'])

    def test_multi_on_file(self):
        '''Tests multiple ignores split and passed for single file'''
        main((self.test_file, '--ignore', 'W1003,E2004'))
        self.analyser.analyse_file.assert_called_once_with(self.test_file, output_tree=False, ignore_list=['E2004', 'W1003'])

    def test_passed_for_dir(self):
        '''Tests that ignore is passed for a directory'''
        self.assertGreater(len(self.test_dir_files), 0)
        main((self.test_dir, '--ignore', 'W1003,E2004'))
        self.assertEqual(len(self.test_dir_files), self.analyser.analyse_file.call_count)
        for call_args in self.analyser.analyse_file.call_args_list:
            self.assertEqual(call_args.kwargs['ignore_list'], ['E2004', 'W1003'])

    def test_exception_on_unknown_messageid(self):
        '''Show an exception is raised when an unknown messageid is passed'''
        with self.assertRaises(AssertionError):
            main((self.test_file, '--ignore', 'W1003,E5000'))
