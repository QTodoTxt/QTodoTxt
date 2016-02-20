from datetime import datetime, date
import re


class TaskHtmlizer(object):
    def __init__(self):
        self.priority_colors = dict(
            A='red',
            B='green',
            C='navy')
        # regex matching creation and completion dates and priority
        self.regex = re.compile(
            r'^(x (?P<completed>\d{4}-\d{2}-\d{2} )?)?(\((?P<priority>[A-Z])\) )?(?P<created>\d{4}-\d{2}-\d{2} )?.*$')

    def task2html(self, task):
        text = task.text
        priority = task.priority

        if task.is_complete:
            text = '<s>%s</s>' % text.replace('x ', '', 1)
            # when the task is complete, the Task object has no priority. We find the original priority from the text
            priority = re.match(self.regex, task.text).group('priority')
        for context in task.contexts:
            text = text.replace('@' + context, self._htmlizeContext(context))
        for project in task.projects:
            text = text.replace('+' + project, self._htmlizeProject(project))
        if priority:
            text = text.replace('(%s) ' % priority, self._htmlizePriority(priority))
        else:
            # add space, so tasks get evenly aligned when there's no priority
            text = '<tt>&nbsp;&nbsp;&nbsp;</tt>&nbsp;' + text
        if task.due:
            text = text.replace('due:{}'.format(task.due), self._htmlizeDueDate(task.due))
        elif task.due_error:
            text = text.replace('due:{}'.format(task.due_error), '<b><font style="color:red">*** Invalid date format, expected: YYYY-mm-dd! due:{}s ***</font></b>'.format(task.due_error))

        if task.threshold:
            text = text.replace('t:%s' % task.threshold, self._htmlizeThresholdDate(task.threshold))
        elif task.threshold_error:
            text = text.replace('t:{}'.format(task.threshold_error), '<b><font style="color:red">*** Invalid date format, expected: YYYY-mm-dd! t:{} ***</font></b>'.format(task.threshold_error))
        text = self._htmlizeCreatedCompleted(text, task.text)
        text = self._htmlizeURL(text)
        return text

    def _htmlizeContext(self, context):
        return '<font color="green">@%s</font>' % context

    def _htmlizeProject(self, project):
        return '<font style="color:#64AAD0">+%s</font>' % project

    def _htmlizePriority(self, priority):
        if priority in self.priority_colors:
            color = self.priority_colors[priority]
            return '<font color="{}"><tt>({})</tt>&nbsp;</font>'.format(color, priority)
        return '<tt>(%s)</tt>&nbsp;' % priority

    def _htmlizeDueDate(self, due_date):
        date_now = date.today()
        tdelta = due_date - date_now
        if tdelta.days > 7:
            return '<b>due:{}</b>'.format(due_date)
        elif tdelta.days > 0:
            return '<b><font color="orange">due:{}</font></b>'.format(due_date)
        else:
            return '<b><font style="color:red">due:{}</font></b>'.format(due_date)

    def _htmlizeThresholdDate(self, threshold):
        date_now = date.today()
        tdelta = threshold - date_now
        if tdelta.days > 0:
            return '<i><font style="color:grey">t:{}</font></i>'.format(threshold)
        else:
            return '<font style="color:orange">t:{}</font>'.format(threshold)

    def _htmlizeURL(self, text):
        regex = re.compile(
            r'((?:http|ftp)s?://'  # TODO what else is supported by xgd-open?
            # TODO add support for user:password@-scheme
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+))(\s|$)', re.IGNORECASE)
        return regex.sub(r'<a href="\1">\1</a>\2', text)

    def _htmlizeCreatedCompleted(self, text, raw_text):
        created = ''
        completed = ''
        match = re.match(self.regex, raw_text)
        if match.group("completed"):
            completed = match.group("completed")
            text = text.replace(completed, '', 1)
        if match.group("created"):
            created = match.group("created")
            text = text.replace(created, '', 1)
        if created or completed:
            first = True
            text += ' <font color="gray">('
            if created:
                text += created.rstrip()
                first = False
            if completed:
                if not first:
                    text += ', '
                text += 'completed: %s' % completed.rstrip()
            text = text + ')</font>'

        return text
