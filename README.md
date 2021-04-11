# GoTestRunner

GoTestRunner is a SublimeText 3 Plugin for running go tests. 

It exposes four commands:

* Run Go Test
* Run Go Test File
* Run Go Package Tests
* Rerun Last Go Test

## Installation

This is not currently published in the plugin directory so you need to install it manually. 

This project needs to be placed in `~/Library/Application Support/Sublime Text 3/Packages`
If you want to be able to hack on it, I recommend checking out this project and then linking it in:

```
git clone github.com/macrael/GoTestRunner
ln -s GoTestRunner ~/Library/Application Support/Sublime\ Text\ 3/Packages/GoTestRunner
```

## Usage

You can run any of the commands via the command palate by hitting cmd-shift-P and typing in one of their names. 

You can add a shortcut by going to Sublime Text > Preferences > Key Bindings and adding lines like this:

```
{ "keys": ["super+shift+;"], "command": "run_go_test"},
{ "keys": ["super+shift+'"], "command": "rerun_last_go_test"},
```

## Credits
In order to determine the test name from the current line number, this plugin includes a copy of https://github.com/jim/wtfunc

Future work could combine them and include a build step.
