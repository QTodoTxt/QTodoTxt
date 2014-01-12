class BaseFilter(object):
    def __init__(self, text):
        self.text = text
    def isMatch(self, task):
        return True
    def __eq__(self, other):
        if not other:
            return False
        if type(other) == type(self):
            return self.text == other.text
        return False

class IncompleteTasksFilter(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self, 'Incomplete')
    def isMatch(self, task):
        return not task.is_complete

class UncategorizedTasksFilter(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self, 'Uncategorized')
    def isMatch(self, task):
        return (not task.is_complete) and (not task.contexts) and (not task.projects)

class CompleteTasksFilter(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self, 'Complete')
        
    def isMatch(self, task):
        return task.is_complete
        
class ContextFilter(BaseFilter):
    def __init__(self, context):
        BaseFilter.__init__(self, context)
        
    def isMatch(self, task):
        return (not task.is_complete) and (self.text in task.contexts)
    
    def __str__(self):
        return "ContextFilter(%s)" % self.text

class ProjectFilter(BaseFilter):
    def __init__(self, project):
        BaseFilter.__init__(self, project)
        
    def isMatch(self, task):
        return (not task.is_complete) and (self.text in task.projects)

    def __str__(self):
        return "ProjectFilter(%s)" % self.text

class HasProjectsFilter(BaseFilter):
    
    def __init__(self):
        BaseFilter.__init__(self, 'Projects')
        
    def isMatch(self, task):
        return (not task.is_complete) and task.projects

    def __str__(self):
        return "HasProjectsFilter" % self.text

class HasContextsFilter(BaseFilter):
    
    def __init__(self):
        BaseFilter.__init__(self, 'Contexts')
        
    def isMatch(self, task):
        return (not task.is_complete) and task.contexts

    def __str__(self):
        return "HasContextsFilter" % self.text

class SimpleTextFilter(BaseFilter):
    
    def __init__(self,text):
        BaseFilter.__init__(self, text)
        
    def isMatch(self,task):
        return (self.text in task.text)
    
    def __str__(self):
        return "SimpleTextFilter(%s)" % self.text
    
class FutureFilter(BaseFilter):
    
    def __init__(self):
        BaseFilter.__init__(self,'Future')

    def isMatch(self, task):
        return not task.is_future
    
    def __str__(self):
        return "FutureFilter " % self.text