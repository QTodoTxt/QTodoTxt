# Contributor's guide

Before you submit any code, make sure to run the `qtodotxt/test/run-tests.py`-script. You can also consider the
`…/run-coverage.py`-script to get find code that is uncovered by tests.

If you are fixing a bug, also write a test that would reproduce the bug in case of failure if possible.

When introducing enhancements, beside a set of tests that fully cover their proper functionality and catch any failure
that can be anticipated, make also sure your code is reasonably documented. For enhancements that should be reflected in
the [user-documentation](https://github.com/mNantern/QTodoTxt/wiki), please provide a suggestion in your pull request.

*The usage of doctests is deprecated and will not be accepted.*

Before committing you should check the code-quality with
[flake8](https://pypi.python.org/pypi/flake8/):

    …/QTodoTxt $ flake8 qtodotxt

If *flake8* is installed, the `qtodotxt/test/run-tests.py`-script will also run this check.
