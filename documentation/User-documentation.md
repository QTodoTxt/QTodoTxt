# User Documentation
## Prerequisites

If you don't use the package for your distribution, you can still run QTodoTxt without installation but you will need to install manually two things: python and pyside.

To install on Linux:
- Install PySide (in Ubuntu: "sudo apt-get install python3-pyside")

To install on Windows:
- Install [Python 3.4](http://www.python.org/download/)
- Install [PySide (for Python 3.4)](http://qt-project.org/wiki/PySide_Binaries_Windows)

## Run it !
If you installed QTodoTxt with binary package you have an executable in your path. Just run it.

For manual install:
* On Linux: execute 'bin/qtodotxt'
* On Windows: execute 'bin/qtodotxt.pyw'

Command line arguments support:
* -f/--file - allows opening a file from the command line
* -q/--quickadd - opens the add-task dialog and exits the application when done

## Use it!
### Useful shortcuts
* **Create Task**: Insert, Ctrl+n or Ctrl+i
* **Delete Task**: Delete
* **Complete Task**: c or x
* **Edit Task**: Enter
* **Save List**: Strg+S
* **Search Tasks**: Ctrl+f
* **Increase Task Priority**: +
* **Decrease Task Priority**: -

### Behaviour description
* **Hyperlinks**: Are recognized automatically if starting with 'http://', 'https://', 'ftp://', etc.
* **Sorting**: Is done automatically at first on priorities and within this order alphabetically
* **Due dates format**: "due:YYYY-MM-DD" (other formats can lead to strange behaviour)
* **Due dates color**: red = today or past; orange = within the following week; black = more than one week

## Tips!
* **Distraction-Free Priorities:**  To focus on a single priority, such as (A) tasks, type (A), A), or (A in the search filter.  Clicking on a project or context will now show just the (A) priorities, which is great if you want to focus on your top priorities without distraction.  Best part is that the filter criteria remains until you reset it!
* **DropBox Integration:**  QTodoTxt works well with DropBox and can now reload automatically your todo.txt file to reflect the last changes (even done outside QTodotxt)

## Issue
* **Upgrade from v1.3 to v1.4:** Normally the upgrade works without issue but sometimes QTodoTxt doesn't start properly after (see [issue #102: v1.4 not run](https://github.com/mNantern/QTodoTxt/issues/102)). To fix that you can rename your config file to start with a new one (if it's still doesn't work, [open an issue](https://github.com/mNantern/QTodoTxt/issues)). Config file is in:
    * C:\Users\<Username>.qtodotxt.cfg on Windows
    * ~/.qtodotxt.cfg on MacOs X and Linux 