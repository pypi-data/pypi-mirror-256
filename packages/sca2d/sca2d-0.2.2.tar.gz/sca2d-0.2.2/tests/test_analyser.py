'''Testing simple parsing examples'''

import unittest
from sca2d import Analyser


class AnalyserTestCase(unittest.TestCase):
    '''Test analyser on simple scripts'''

    def setUp(self):
        '''On setup a ScadParser is setup up for all unit tests'''
        self.analyser = Analyser()

    def test_warn_empty(self):
        '''Check that a file with no scad code warns'''
        snippets = ['',
                    '    ',
                    '/*This is only a comment*/']
        for snippet in snippets:
            success, messages = self.analyser.analyse_code(snippet, ignore_list=['I0006'])
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].code, "W1003")

    def test_assignmnet(self):
        '''Check assignment works as expected'''
        snippet = 'a = 1 + 1 / 2;'
        success, messages = self.analyser.analyse_code(snippet, ignore_list=['I3001'])
        self.assertEqual(success, 1)
        self.assertEqual(len(messages), 0)

    def test_extra_semicolon(self):
        '''Check assignment works as expected'''
        snippet = 'a = 1 + 1 / 2;;'
        success, messages = self.analyser.analyse_code(snippet, ignore_list=['I3001'])
        self.assertEqual(success, 1)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].code, "I0001")

    def test_pointless_scope(self):
        '''Check assignment works as expected'''
        snippet = '{a = 1 + 1 / 2;}'
        success, messages = self.analyser.analyse_code(snippet, ignore_list=['I3001'])
        self.assertEqual(success, 1)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].code, "I0002")

    def test_trailing_whitepace(self):
        '''Check that for warnings from trailing white space'''
        snippets = [' \na=1;',
                    '\n\na=1; ',
                    '\na=1;\n ']
        for snippet in snippets:
            success, messages = self.analyser.analyse_code(snippet, ignore_list=['I3001'])
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].code, "I0006")

    def test_recursive_let_module_pass(self):
        '''Check that you can use one let definition in the
        next one'''
        snippets = ['let (x = 1, y = x + 1)cube([x,y,y]);',
                    'let (x = 1, y = x + 1)cube([y,y,y]);']
        for snippet in snippets:
            success, messages = self.analyser.analyse_code(snippet)
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), 0)

    def test_recursive_let_module_fail(self):
        '''Check let fails if the second definition is unknown'''
        success, messages = self.analyser.analyse_code('let (x = 1, y = z + 1)cube([x,y,y]);')
        self.assertEqual(success, 1)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].code, "E2001")

    def test_recursive_let_module_warn(self):
        '''Check let warns if internal scope doesn't use all assigned vars'''
        success, messages = self.analyser.analyse_code('let (x = 1, y = x + 1)cube([x,x,x]);')
        self.assertEqual(success, 1)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].code, "W2007")

    def test_sequential_assignment_for(self):
        '''Check that you can use one for definition in the next one'''
        code = "for (d = [1,2],c = [d,1])echo(c);"
        success, messages = self.analyser.analyse_code(code)
        self.assertEqual(success, 1)
        self.assertEqual(len(messages), 0)

    def test_recursive_let_expression_pass(self):
        '''This is a let expression which not a let module as they are
        parse differently'''
        snippets = ['echo(let (x = 1, y = x + 1) y+3);']
        for snippet in snippets:
            success, messages = self.analyser.analyse_code(snippet)
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), 0)

    def test_list_comp_variable_usage(self):
        '''Check variable useage is recognised inside a list comprehension'''
        snippets = ['a=3; dims = [for (d = [1,2,3]) d*a]; for (dim = dims) cube([10/dim,dim,dim]);',
                    "echo([for (d = [1,2],c = [d,1]) c]);",
                    'echo([for (d = [1,2,3]) d*d]);',
                    'echo([each [1,2,5]]);',
                    'echo([if (1==2) 4]);',
                    'echo([if (1==2) 3 else 5]);',
                    'echo([for (a = 0, b = a+1;b < 1000;x = a + b, a = b, b = x) a]);',
                    'echo([for (i = [1,2]) let(j = i*2) j*i ]);']

        for snippet in snippets:
            success, messages = self.analyser.analyse_code(snippet, ignore_list=['I1001', 'I1002', 'I3001'])
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), 0)

    def test_function_defintion(self):
        '''Test function definitions work correctly'''
        snippets = ['function A() = let(a = [1,1],b = [for (i=a) i]) b;echo(A());']
        for snippet in snippets:
            success, messages = self.analyser.analyse_code(snippet, ignore_list=['I1001', 'I1002'])
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), 0)

    def test_inline_assert_with_complex_expr(self):
        '''Test assert statments within complex expressons'''
        snippets = ['a=[1,2];echo(assert(is_list(a), "msg")let(b = a+[1,1], c = [for (i = b) if (i>2) 0 else a]) c+1);',
                    'a=[1,2,3];z=let(b = [for (i = a) assert(i<4, "msg") i+1 ])b;echo(z);']
        for snippet in snippets:
            success, messages = self.analyser.analyse_code(snippet, ignore_list=['I1001', 'I3001'])
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), 0)

    def test_inline_assert_with_complex_expr_and_undefined_var(self):
        '''Test assert statment in a complex expression does not affect undefined variables'''
        snippets = ['a=[1,2];echo(assert(is_list(a), "msg")let(b = a+[1,1], c = [for (i = b) if (i>2) 0 else a]) c+z);',
                    'a=[1,2,3];z=let(b = [for (i = a) assert(i<4, "msg") i+k ])b;echo(z);']
        for snippet in snippets:
            success, messages = self.analyser.analyse_code(snippet, ignore_list=['I1001', 'I3001'])
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].code, "E2001")

    def test_functions_with_named_args(self):
        '''Check that named arguments in functions are not recognised as used variables'''
        snippets = ['echo(sin(degrees=90));', 'echo(sin(degrees=90)+2);']
        for snippet in snippets:
            success, messages = self.analyser.analyse_code(snippet, ignore_list=['I1001', 'I3001'])
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), 0)

    def test_empty_arg_function_module(self):
        '''Check that warning is generated if there is an empty argument in a function call'''
        snippets = ['cylinder(1,,2);',
                    'cylinder(1,2,);',
                    'echo(concat(1,2,,4));',
                    'echo(concat(1,2,4,));']
        for snippet in snippets:
            success, messages = self.analyser.analyse_code(snippet)
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].code, "E0004")

    def test_empty_function_module(self):
        '''Check that no argument in a function call is valid'''
        snippets = ['cube();']
        for snippet in snippets:
            success, messages = self.analyser.analyse_code(snippet)
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), 0)

    def test_empty_item_list(self):
        '''Check that an error us generated if a list has a missing item'''
        snippets = ['a = [1,,2];']
        for snippet in snippets:
            success, messages = self.analyser.analyse_code(snippet, ignore_list=['I3001'])
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].code, "E0005")

    def test_empty_list_and_trailing_comma(self):
        '''Check that the missing item error is not generated for an empty list or trailing comma'''
        snippets = ['a = [];', 'a = [1,2,];']
        for snippet in snippets:
            success, messages = self.analyser.analyse_code(snippet, ignore_list=['I3001'])
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), 0)

    def test_attributes(self):
        '''Check that using .x, .y or .z attributed do not cause errors to be thrown'''
        snippets = ['a = [1,2,3];b=a.x;']
        for snippet in snippets:
            success, messages = self.analyser.analyse_code(snippet, ignore_list=['I3001'])
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), 0)

    def test_invalid_attributes(self):
        '''Check that an error is thrown for any attribute that is not .x .y or .z'''
        snippets = ['a = [1,2,3];b=a.d;']
        for snippet in snippets:
            success, messages = self.analyser.analyse_code(snippet, ignore_list=['I3001'])
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].code, "E2004")

    def test_function_literal(self):
        '''Check that a function literal can be declared and used'''
        snippet = 'double = function(x) x*2;echo(double(3));'
        success, messages = self.analyser.analyse_code(snippet, ignore_list=['I3001'])
        self.assertEqual(success, 1)
        self.assertEqual(len(messages), 0)

    def test_caret_power(self):
        '''Check that a ^ symbol can be used for power'''
        snippet = 'echo(3^3);'
        success, messages = self.analyser.analyse_code(snippet)
        self.assertEqual(success, 1)
        self.assertEqual(len(messages), 0)

    def test_redefine_variable_within_scope(self):
        '''Check that a waring if thrown if variable is redefined within scope'''
        snippet = 'a=1;a=2;'
        success, messages = self.analyser.analyse_code(snippet, ignore_list=['I3001'])
        self.assertEqual(success, 1)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].code, "W2001")

    def test_redefine_outer_variable_in_module_def(self):
        '''Check that a warning if thrown if variable is redefined by a module defintion'''
        snippets = ['foo=1; module bar(){foo=2;cube(foo);}',
                    'foo=1; module bar(foo=2){cube(foo);}']
        for snippet in snippets:
            success, messages = self.analyser.analyse_code(snippet, ignore_list=['I3001'])
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].code, "W2002")

    def test_redefine_module_inputs_within_scope(self):
        '''
        Check that a warning is thrown if redefining inputs withing a module defintion
        unless is keyword that defaults to undef
        '''
        snippets_with_code = [['module bar(foo){cube(foo);}', None],
                              ['module bar(foo){foo=2;cube(foo);}', 'W2013'],
                              ['module bar(foo=4){foo=2;cube(foo);}', 'W2014'],
                              ['module bar(foo=undef){foo=2;cube(foo);}', None]]
        for snippet, code in snippets_with_code:
            success, messages = self.analyser.analyse_code(snippet, ignore_list=['I3001'])
            self.assertEqual(success, 1)
            if code is None:
                self.assertEqual(len(messages), 0)
            else:
                self.assertEqual(len(messages), 1)
                self.assertEqual(messages[0].code, code)

    def _base_test_module_call_arguments(self, module_def_code, calls_with_codes):
        for call, codes in calls_with_codes:
            snippet = module_def_code+call
            success, messages = self.analyser.analyse_code(snippet, ignore_list=['I3001'])
            self.assertEqual(success, 1)
            self.assertEqual(len(messages), len(codes))
            message_codes = [msg.code for msg in messages]
            for code in codes:
                self.assertIn (code, message_codes)

    def test_module_call_arguments1(self):
        '''
        Check that a warning is thrown if redefining inputs withing a module defintion
        unless is keyword that defaults to undef
        '''
        module_def_code = 'module bar(foo=2){cube(foo);}'

        calls_with_codes = [['bar();', []],
                            ['bar(22);', []],
                            ['bar(foo=22);', []],
                            ['bar(22, 44);', ['W3001']],
                            ['bar(boo=22);', ['W3003']]]

        self._base_test_module_call_arguments(module_def_code, calls_with_codes)

    def test_module_call_arguments2(self):
        '''
        Check that a warning is thrown if redefining inputs withing a module defintion
        unless is keyword that defaults to undef
        '''
        module_def_code = 'module bar(foo){cube(foo);}'

        calls_with_codes = [['bar();', ['W3002']],
                            ['bar(22);', []],
                            ['bar(foo=22);', []],
                            ['bar(22, 44);', ['W3001']],
                            ['bar(boo=22);', ['W3003', 'W3004']]]

        self._base_test_module_call_arguments(module_def_code, calls_with_codes)

    def test_module_call_arguments3(self):
        '''
        Check that a warning is thrown if redefining inputs withing a module defintion
        unless is keyword that defaults to undef
        '''
        module_def_code = 'module bar(foo, foo2=1){cube([foo, foo, foo2]);}'

        calls_with_codes = [['bar();', ['W3002']],
                            ['bar(22);', []],
                            ['bar(foo=22);', []],
                            ['bar(22, 44);', []],
                            ['bar(boo=22);', ['W3003', 'W3004']],
                            ['bar(foo2=22);', ['W3004']],
                            ['bar(17, foo=22);', ['W3005']]]

        self._base_test_module_call_arguments(module_def_code, calls_with_codes)
