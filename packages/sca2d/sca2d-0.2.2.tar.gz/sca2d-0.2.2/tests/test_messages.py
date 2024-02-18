'''Testing simple parsing examples'''
import io
import unittest
import unittest.mock
import re
from colorama import Fore, Style
from sca2d import messages, scadclasses

class PrintMessagesTestCase(unittest.TestCase):
    '''Test printing messages or message summary to screen'''

    def test_msg_print(self):
        msg = messages.Message('nofile.scad', 'I0001', scadclasses.DummyTree())
        self.assertTrue(str(msg).startswith('nofile.scad:1:1:'))

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_messages1(self, mock_stdout):
        msg1 = messages.Message('nofile.scad', 'I0001', scadclasses.DummyTree())
        msg2 = messages.Message('nofile.scad', 'E0001', scadclasses.DummyTree())
        msgs = [msg1, msg2]
        buffer_pos = 0
        for colour in [True, False]:
            messages.print_messages(msgs, 'nofile.scad', colour=colour)
            printed = mock_stdout.getvalue()[buffer_pos:]
            buffer_pos += len(printed)
            self.assertTrue(printed.startswith('nofile.scad:1:1:'))
            if colour:
                self.assertTrue(printed.endswith(Style.RESET_ALL+'\n'))
                self.assertTrue(Fore.RED in printed)
            else:
                self.assertFalse(printed.endswith(Style.RESET_ALL+'\n'))
                self.assertFalse(Fore.RED in printed)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_print_messages2(self, mock_stdout):
        buffer_pos = 0
        for colour in [True, False]:
            messages.print_messages([], 'nofile.scad', colour=colour)
            printed = mock_stdout.getvalue()[buffer_pos:]
            buffer_pos += len(printed)
            pass_msg = 'nofile.scad passed all checks!'
            if colour:
                colour_msg = Fore.GREEN + pass_msg + Style.RESET_ALL + '\n'
                self.assertEqual(printed, colour_msg)
            else:
                self.assertEqual(printed, pass_msg+'\n')

    def test_message_summary(self):
        msg1 = messages.Message('nofile.scad', 'I0001', scadclasses.DummyTree())
        msg2 = messages.Message('nofile.scad', 'E0001', scadclasses.DummyTree())
        msgs = [msg1, msg2]
        summary = messages.count_messages(msgs)
        self.assertTrue(isinstance(summary, messages.MessageSummary))
        self.assertEqual(summary.fatal, 0)
        self.assertEqual(summary.error, 1)
        self.assertEqual(summary.info, 1)
        err_warn_strs = re.findall(r'^Errors: *1$', str(summary), re.MULTILINE)
        self.assertEqual(len(err_warn_strs), 1)

