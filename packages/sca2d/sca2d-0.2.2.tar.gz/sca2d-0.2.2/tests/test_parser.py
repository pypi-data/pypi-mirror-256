'''Testing simple parsing examples'''

import unittest
from sca2d import ScadParser


class ParserTestCase(unittest.TestCase):
    '''Simple parsing example. Not real-world scripts'''

    def setUp(self):
        '''On setup a ScadParser is setup up for all unit tests'''
        self.parser = ScadParser()

    def test_empty(self):
        '''Tests an empty file'''
        self.parser.parse('')

    def test_assignmnet(self):
        '''Tests simple assignment, currently only fails if there is a
        parse error'''
        self.parser.parse('a = 1 + 1 / 2;')

    def test_empty_scope(self):
        '''Tests simple assignment, currently only fails if there is a
        parse error'''
        self.parser.parse('a = 1 + 1 / 2;\n{}')

    def test_module_chain(self):
        '''Parse modules chained together in different ways.'''
        tree = self.parser.parse('foo(a,b)bar();')
        tree2 = self.parser.parse('foo(a,b){bar();}')
        self.assertEqual(tree,tree2)

    def test_module_definition(self):
        '''Check different ways of defining a module parse
        and incorrect ones don't'''
        tree = self.parser.parse('module bar(){cube([1,2,3]);}')
        self.assertIn('module_def', tree.pretty())

        tree = self.parser.parse('modulebar(){cube([1,2,3]);}')
        self.assertNotIn('module_def', tree.pretty())
