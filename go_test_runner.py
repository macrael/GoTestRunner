import sublime
import sublime_plugin

import subprocess
import os

last_run_test = None

class RerunLastGoTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_regex = "^\\s*(\\S[^:]*):(\\d+): ([^\\n]+)"
        self.view.window().run_command("exec", {"cmd": ["go", "test", "-run", last_run_test], "quiet": True, "file_regex": file_regex})


# PACKAGE, FILE, TEST
class RunGoTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selected_regions = self.view.sel()
        first_selection_leading_edge = selected_regions[0].a
        cursor_line = self.view.rowcol(first_selection_leading_edge)[0] + 1

        this_dir = os.path.dirname(os.path.abspath(__file__))
        wtfunc_path = os.path.join(this_dir, "wtfunc")

        # TODO: error handling, with some visible output when you mess up
        result = subprocess.check_output([wtfunc_path, "-line", str(cursor_line), self.view.file_name()])
        test_name = result.decode('UTF-8')

        # file_regex adds "build" errors inline and lets you double click on an error line in the panel to jump there
        file_regex = "^\\s*(\\S[^:]*):(\\d+): ([^\\n]+)"
        self.view.window().run_command("exec", {"cmd": ["go", "test", "-run", test_name], "quiet": True, "file_regex": file_regex})
        global last_run_test
        last_run_test = test_name
