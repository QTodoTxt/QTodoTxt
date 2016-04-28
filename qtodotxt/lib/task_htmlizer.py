from datetime import date
import re


class TaskHtmlizer(object):

    def __init__(self):
        self.priority_colors = dict(
            A='red',
            B='green',
            C='navy')

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
                word = self._addUrl(word)
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
            html += ' <font color="gray">(completed: {})</font>'.format(task.completion_date)
        if task.creation_date:
            html += ' <font color="gray">(created: {})</font>'.format(task.creation_date)
        return html

    def _addUrl(self, word, color="none"):
        cleanWord = re.sub(r"https?://", "", word)
        word = '<a style="color:' + color + ';" href="{}">{}</a>'.format(word, cleanWord)

        return word

    def _htmlizeContext(self, context):
        context = context.replace("@", "")
        if "://" in context:
            context = self._addUrl(context, "green")

        return '<font style="color:green">@%s</font>' % context

    def _htmlizeProject(self, project):
        project = project.replace("+", "")
        if "://" in project:
            project = self._addUrl(project, "#64AAD0")

        return '<font style="color:#64AAD0">+%s</font>' % project

    def _htmlizePriority(self, priority):
        if priority in self.priority_colors:
            color = self.priority_colors[priority]
            return '<font style="color:{}"><tt>({})</tt>&nbsp;</font>'.format(color, priority)
        return '<tt>(%s)</tt>&nbsp;' % priority

    def _htmlizeDueDate(self, task, string):
        if not task.due:
            return ('<b><font style="color:red">*** {}'
                    ' Invalid date format, expected YYYY-MM-DD. ***</font></b>'.format(string))

        date_now = date.today()
        tdelta = task.due - date_now
        if tdelta.days > 7:
            return '<b>due:{}</b>'.format(task.due)
        elif tdelta.days > 0:
            return '<b><font style="color:orange">due:{}</font></b>'.format(task.due)
        else:
            return '<b><font style="color:red">due:{}</font></b>'.format(task.due)

    def _htmlizeThresholdDate(self, task, string):
        if not task.threshold:
            return ('<b><font style="color:red">*** {}'
                    ' Invalid date format, expected YYYY-MM-DD. ***</font></b>'.format(string))

        date_now = date.today()
        tdelta = task.threshold - date_now
        if tdelta.days > 0:
            return '<i><font style="color:grey">t:{}</font></i>'.format(task.threshold)
        else:
            return '<font style="color:orange">t:{}</font>'.format(task.threshold)
