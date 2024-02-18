'''Testing simple parsing examples'''

import os
import unittest
from sca2d import Analyser

class FileAnalysisTestCase(unittest.TestCase):
    '''Testing the analyser on actual scad files'''

    def setUp(self):
        '''On setup a ScadParser is setup up for all unit tests'''
        self.analyser = Analyser()
        self.scadfile_path = os.path.join('tests','scadfiles')

    def test_use_import_global(self):
        '''Check that a file with no scad code warns'''
        filename = os.path.join(self.scadfile_path, 'test_use_import_global.scad')
        success, messages = self.analyser.analyse_file(filename)
        self.assertEqual(success, 1)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].code, "E2001")

    def test_include_import_global(self):
        '''Check that a file with no scad code warns'''
        filename = os.path.join(self.scadfile_path, 'test_include_import_global.scad')
        success, messages = self.analyser.analyse_file(filename)
        self.assertEqual(success, 1)
        self.assertEqual(len(messages), 0)

    def test_use_unneeded(self):
        '''Check that a file with no scad code warns'''
        filename = os.path.join(self.scadfile_path, 'test_use_unneeded.scad')
        success, messages = self.analyser.analyse_file(filename)
        self.assertEqual(success, 1)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].code, "W1001")
