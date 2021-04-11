import sublime
import sublime_plugin

import subprocess
import os

# Testrun: type: 'PACKAGE, FILE, TEST', file_names / test_name / working_dir
last_testrun = None

# This helper does the work of saving the previous invocation regardless of the calling command
def run_go_tests(window, testrun):
    test_args = []

    if testrun['type'] == 'TEST':
        test_args = ['-run', testrun['test_name']]
    elif testrun['type'] == 'FILE':
        test_args = testrun['file_paths']
    elif testrun['type'] != 'PACKAGE':
        raise RuntimeError('invalid testrun type ' + testrun['type'])

    working_dir = testrun['working_dir']

    cmd_args = ['go', 'test'] + test_args

    file_regex = '^\\s*(\\S[^:]*):(\\d+): ([^\\n]+)'
    window.run_command('exec', {'cmd': cmd_args, 'quiet': True, 'file_regex': file_regex, 'working_dir': working_dir})
    global last_testrun
    last_testrun = testrun

# run_go_package_tests runs all the tests in the given package
class RunGoPackageTestsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        working_dir = os.path.dirname(self.view.file_name())

        test_cmd = {
            'type': 'PACKAGE',
            'working_dir': working_dir,
        }

        run_go_tests(self.view.window(), test_cmd)


# run_go_test_file runs all the tests in the open file
class RunGoTestFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        working_dir = os.path.dirname(self.view.file_name())

        # SO. The `go test foo_test.go` command has funny behavior. 
        # https://stackoverflow.com/questions/16935965/how-to-run-test-cases-in-a-specified-file
        # to best guarantee that we can run all the tests in a single test file, we pass
        # a list of every file that doesn't end with `_test.go` in addition to the one
        # test file the cursor is presently in. 
        non_test_files = [ f for f in os.listdir(working_dir) if os.path.isfile(f) and not f.endswith('_test.go') ]

        # add the one test file we want to test into the mix
        test_file = os.path.basename(self.view.file_name())
        if not test_file.endswith('_test.go'):
            self.view.window().status_message('GoTestRunner: Error: this file does not appear to be a test.')
            return

        test_files = non_test_files + [test_file]

        test_cmd = {
            'type': 'FILE',
            'working_dir': working_dir,
            'file_paths': test_files,
        }

        run_go_tests(self.view.window(), test_cmd)

# run_go_test runs a single go test that's under the cursor
class RunGoTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selected_regions = self.view.sel()
        first_selection_leading_edge = selected_regions[0].a
        cursor_line = self.view.rowcol(first_selection_leading_edge)[0] + 1

        this_dir = os.path.dirname(os.path.abspath(__file__))
        wtfunc_path = os.path.join(this_dir, 'wtfunc')

        try:
            result = subprocess.check_output([wtfunc_path, '-line', str(cursor_line), self.view.file_name()])
            test_name = result.decode('UTF-8')

            working_dir = os.path.dirname(self.view.file_name())

            test_cmd = {
                'type': 'TEST',
                'working_dir': working_dir,
                'test_name': test_name
            }

            run_go_tests(self.view.window(), test_cmd)
        except subprocess.CalledProcessError:
            # There can probably be other reasons for wtfunc to fail, but this is the most likely
            self.view.window().status_message('GoTestRunner: Error: Cursor does not appear to be in a test.')

# rerun_last_go_test runs the previous test invocation, whatever it was, again.
class RerunLastGoTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if last_testrun == None:
            self.view.window().status_message('GoTestRunner: Error: No test run to rerun')

        run_go_tests(self.view.window(), last_testrun)
