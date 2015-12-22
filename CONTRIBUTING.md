# Contributor's guide

Before you submit any code, make sure to run the following tests before committing:

    …/QTodoTxt $ flake8 qtodotxt
    …/QTodoTxt $ py.test qtodotxt/test 
    …/QTodoTxt $ qtodotxt/test/run-tests.py 

As PySide must be compiled on [Travis](https://travis-ci.org/mNantern/QTodoTxt), the tests there will run a considerably 
long time. Please refer to [flake8](https://flake8.readthedocs.org)'s and [pytest](https://pytest.org)'s documentation 
for details on these tests. You can also consider the `…/run-coverage.py`-script to get find code that is uncovered by 
tests.

If you are fixing a bug, also write a test that would reproduce the bug in case of failure if possible.

When introducing enhancements, beside a set of tests that fully cover their proper functionality and catch any failure
that can be anticipated, make also sure your code is reasonably documented. For enhancements that should be reflected in
the [user-documentation](https://github.com/mNantern/QTodoTxt/wiki), please provide a suggestion in your pull request.

**The usage of doctests is deprecated and will not be accepted.**
