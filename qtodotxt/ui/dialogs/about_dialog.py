from PyQt5 import QtWidgets


__version__ = "1.6.1"

description = """<p>QTodoTxt is a cross-platform UI client for todo.txt files
 (see <a href="http://todotxt.com">http://todotxt.com</a>)</p>

Copyright &copy; David Elentok 2011<br/>
Copyright &copy; Matthieu Nantern 2013-2015<br/>
Copyright &copy; QTT Development Team 2015-2016

<h2>Links</h2>
<ul>
<li>Project Page: <a href="https://github.com/QTodoTxt/QTodoTxt">https://github.com/QTodoTxt/QTodoTxt</a></li>
</ul>

<h2>Credits</h2>

<ul>
    <li>Concept by <a href="http://ginatrapani.org/">Gina Trapani</a></li>
    <li>Icons by <a href="http://tango.freedesktop.org/">The Tango! Desktop Project</a>
        and <a href="http://www.famfamfam.com/lab/icons/silk/">Mark James</a></li>
    <li>Original code by <a href="http://elentok.blogspot.com">David Elentok</a></li>
</ul>

<h2>License</h2>

<p>This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.</p>

<p>This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.</p>

<p>You should have received a copy of the GNU General Public License
along with this program.  If not, see
<a href="http://www.gnu.org/licenses/">http://www.gnu.org/licenses/</a>.</p>
"""


def _getAboutText():
    parts = ["<h1>About QTodoTxt %s</h1>\n" % __version__, description]
    return ''.join(parts)


def show(parent=None):
    text = _getAboutText()
    QtWidgets.QMessageBox.information(parent, 'About QTodoTxt', text)
