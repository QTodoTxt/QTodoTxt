from datetime import date
import re
from PyQt5 import QtCore


class TaskHtmlizer(object):

    def __init__(self):
        colorSchemName = QtCore.QSettings().value("color_schem", "")
        if str(colorSchemName).find("dark") >= 0:   # for dark theme
            self.priority_colors = dict(
                A='red',
                B='#1C7F61',
                C='#7397BE')
            self.contextColor = "#5ED2B8"
            self.projectColor = "#FFCA73"
            self.priorityDuecolors = ['red', '#E0A180']
            self.priorityThresholdColors = ['orange', 'grey']
            self.errorColor = "red"
            self.linkColor = "#E0A180"
        else:                                    # for light theme
            self.priority_colors = dict(
                A='red',
                B='green',
                C='navy')
            self.contextColor = "green"
            self.projectColor = "#64AAD0"
            self.priorityDuecolors = ['red', 'orange']
            self.priorityThresholdColors = ['orange', 'grey']
            self.errorColor = "red"
            self.linkColor = "none"

        self.complColor = "gray"

    def task2html(self, task):
        words = task.description.split(" ")
        newwords = []
        for word in words:
            if word.startswith("@"):
                word = self._htmlizeContext(word)
            elif word.startswith("+"):
                word = self._htmlizeProject(word)
            elif word.startswith("due:"):
                word = self._htmlizeDueDate(task, word)
            elif word.startswith("t:"):
                word = self._htmlizeThresholdDate(task, word)
            elif "://" in word:
                word = self._addUrl(word, self.linkColor)
            newwords.append(word)
        html = " ".join(newwords)
        if task.is_complete:
            html = '<s>{}</s>'.format(html)
        if task.priority:
            html = self._htmlizePriority(task.priority) + html
        else:
            # add space, so tasks get evenly aligned when there's no priority
            html = '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;' + html
        if task.completion_date:
            html += ' <font color="{1!s}">(completed: {0!s})</font>'.format(task.completion_date, self.complColor)
        if task.creation_date:
            html += ' <font color="{1!s}">(created: {0!s})</font>'.format(task.creation_date, self.complColor)
        return html

    def _addUrl(self, word, color="none"):
        cleanWord = re.sub(r"https?://", "", word)
        word = '<a style="color:{2!s};" href="{0!s}">{1!s}</a>'.format(word, cleanWord, color)

        return word

    def _htmlizeContext(self, context):
        context = context.replace("@", "")
        if "://" in context:
            context = self._addUrl(context, self.contextColor)

        return '<font style="color:{0!s}">@{1!s}</font>'.format(self.contextColor, context)

    def _htmlizeProject(self, project):
        project = project.replace("+", "")
        if "://" in project:
            project = self._addUrl(project, self.projectColor)

        return '<font style="color:{0!s}">+{1!s}</font>'.format(self.projectColor, project)

    def _htmlizePriority(self, priority):
        if priority in self.priority_colors:
            color = self.priority_colors[priority]
            return '<font style="color:{}"><tt>({})</tt>&nbsp;</font>'.format(color, priority)
        return '<tt>(%s)</tt>&nbsp;' % priority

    def _htmlizeDueDate(self, task, string):
        if not task.due:
            return ('<b><font style="color:{1!s}">*** {0!s}'
                    ' Invalid date format, expected YYYY-MM-DD. ***</font></b>'.format(string, self.errorColor))

        date_now = date.today()
        tdelta = task.due - date_now
        if tdelta.days > 7:
            return '<b>due:{}</b>'.format(task.due)
        elif tdelta.days > 0:
            return '<b><font style="color:{1!s}">due:{0!s}</font></b>'.format(task.due, self.priorityDuecolors[1])
        else:
            return '<b><font style="color:{1!s}">due:{0!s}</font></b>'.format(task.due, self.priorityDuecolors[0])

    def _htmlizeThresholdDate(self, task, string):
        if not task.threshold:
            return ('<b><font style="color:{1!s}">*** {0!s}'
                    ' Invalid date format, expected YYYY-MM-DD. ***</font></b>'.format(string, self.errorColor))

        date_now = date.today()
        tdelta = task.threshold - date_now
        if tdelta.days > 0:
            return '<i><font style="color:{1!s}">t:{0!s}</font></i>'.\
                format(task.threshold, self.priorityThresholdColors[1])
        else:
            return '<font style="color:{1!s}">t:{0!s}</font>'.\
                format(task.threshold, self.priorityThresholdColors[0])
