from datetime import datetime, date
import re

class TaskHtmlizer(object):
    def __init__(self):
        self.priority_colors = dict(
            A='red',
            B='green',
            C='cyan')
        # regex matching creation and completion dates and priority
        self.regex = re.compile(
            r'^(x (?P<completed>\d{4}-\d{2}-\d{2} )?)?(\((?P<priority>[A-Z])\) )?(?P<created>\d{4}-\d{2}-\d{2} )?.*$')
    
    def task2html(self, task, selected = False):
        text = task.text
        priority = task.priority

        if task.is_complete:
            text = '<s>%s</s>' % text.replace('x ', '', 1)
            # when the task is complete, the Task object has no priority. We find the original priority from the text
            priority = re.match(self.regex, task.text).group('priority')
        
        if selected:
            text = '<font color="white">%s</font>' % text
        else:
            text = '<font color="black">%s</font>' % text
        
        for context in task.contexts:
            text = text.replace('@' + context, self._htmlizeContext(context))
        for project in task.projects:
            text = text.replace('+' + project, self._htmlizeProject(project))
        if priority is not None:
            text = text.replace('(%s) ' % priority, self._htmlizePriority(priority))
        else:
            # add 3 spaces, so tasks get evenly aligned when there's no priority
            text = '<font face="Lucida Console,monospace,Ubuntu Mono">&nbsp;&nbsp;&nbsp;</font>' + text
        if task.due is not None:
            text = text.replace('due:%s' % task.due, self._htmlizeDueDate(task.due))
        if task.threshold is not None:
            text = text.replace('t:%s' % task.threshold, self._htmlizeThresholdDate(task.threshold))
        text = self._htmlizeCreatedCompleted(text, task.text)

        return self._htmlizeURL(text)
    
    def _htmlizeContext(self, context):
        return '<font color="green">@%s</font>' % context

    def _htmlizeProject(self, project):
        return '<font style="color:#64AAD0">+%s</font>' % project
    
    def _htmlizePriority(self, priority):
        if priority in self.priority_colors:
            color = self.priority_colors[priority]
            return '<font face="Lucida Console,monospace,Ubuntu Mono" color="%s">&nbsp;%s&nbsp;</font>' % (color, priority)
        return '<font face="Lucida Console,monospace,Ubuntu Mono">&nbsp;%s&nbsp;</font>' % priority

    def _htmlizeDueDate(self, dueDateString):
        due_date = datetime.strptime(dueDateString, '%Y-%m-%d').date()
        date_now = date.today()
        tdelta = due_date - date_now
        if tdelta.days > 7:
            return '<b>due:%s</b>' % dueDateString
        elif tdelta.days > 0:
            return '<b><font color="orange">due:%s</font></b>' % dueDateString
        else:
            return '<b><font style="color:red">due:%s</font></b>' % dueDateString

    def _htmlizeThresholdDate(self,thresholdDateString):
        threshold_date = datetime.strptime(thresholdDateString, '%Y-%m-%d').date()
        date_now = date.today()
        tdelta = threshold_date - date_now
        if tdelta.days > 0:
            return '<i><font style="color:grey">t:%s</font></i>' % thresholdDateString
        else:
            return '<font style="color:orange">t:%s</font>' % thresholdDateString

    def _htmlizeURL(self,text):
        regex = re.compile(
            r'((?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:[-_/?a-zA-Z0-9]*))', re.IGNORECASE)
        return regex.sub(r'<a href="\1">\1</a>', text)

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

