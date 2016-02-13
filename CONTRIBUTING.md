# Contributor's guide

## Testing your code
Before you submit any code, make sure to run the following tests before committing:

    …/QTodoTxt $ flake8 qtodotxt
    …/QTodoTxt $ py.test qtodotxt/test
    …/QTodoTxt $ qtodotxt/test/run-doctests.py

If you installed both Python 2 and Python 3 on your system, make sure you run these tests with Python 3.
Depending on your system configuration, the above commands may have to be replaced by commands like these:

    …/QTodoTxt $ python3 -m flake8 qtodotxt
    …/QTodoTxt $ python3 -m py.test qtodotxt/test
    …/QTodoTxt $ qtodotxt/test/run-doctests.py

Please refer to [flake8](https://flake8.readthedocs.org)'s and [pytest](https://pytest.org)'s documentation 
for details on these tests. You can also consider the `…/run-coverage.py`-script to get find code that is uncovered by 
tests.

If you are fixing a bug, also write a test that would reproduce the bug in case of failure if possible.

When introducing enhancements, beside a set of tests that fully cover their proper functionality and catch any failure
that can be anticipated, make also sure your code is reasonably documented. For enhancements that should be reflected in
the [user-documentation](https://github.com/QTodoTxt/QTodoTxt/wiki), please provide a suggestion in your pull request.

**The usage of doctests is deprecated and will not be accepted.**

## Merging rules
This applies especially to group members.

1. Always create a pull request and wait for review. Do not push directly to master (except if you are merging a pull request).
2. If no one disapproves a pull request, you can merge it into the master branch. If someone (especially a group member) disapproves a pull request, wait and find a solution.
3. As a general rule of thumb, you should wait seven days before merging a pull request. For changes with a  bigger impact, you should wait a longer time. For urgent bugfixes the waiting time can be shortened. If one or more group members approve a pull request, the waiting time can be shortened too.
