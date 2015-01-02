import json
import os

DEFAULT_SETTINGS_FILE = os.path.expanduser("~/.qtodotxt.cfg")
UI_MARGINS_OFFSET = -4


class Settings(object):
    def __init__(self):
        self._file = DEFAULT_SETTINGS_FILE
        self._data = {}

    def load(self, filename=DEFAULT_SETTINGS_FILE):
        self._file = filename
        try:
            with open(self._file, 'tr') as file:
                self._data = json.load(file)
        except (ValueError, UnicodeDecodeError):
            import pickle
            with open(self._file, 'br') as file:
                self._data = pickle.load(file)
        except FileNotFoundError:
            self._data = {}
        except:
            raise

    def getLastOpenFile(self):
        return self._getData('last_open_file')

    def setLastOpenFile(self, last_open_file):
        self._setData('last_open_file', last_open_file)

    def getCreateDate(self):
        return self._getData('add_create_date')

    def setCreateDate(self, addCreationDate):
        self._setData('add_create_date', addCreationDate)

    def getAutoSave(self):
        return self._getData('auto_save')

    def setAutoSave(self, autoSave):
        self._setData('auto_save', autoSave)

    def getAutoArchive(self):
        return self._getData('auto_archive')

    def setAutoArchive(self, autoArchive):
        self._setData('auto_archive', autoArchive)

    def getHideFutureTasks(self):
        return self._getData('hide_future_tasks')

    def setHideFutureTasks(self, hideFutureTasks):
        self._setData('hide_future_tasks', hideFutureTasks)
    
    def getSupportMultilineTasks(self):
        return self._getData('support_multiline_tasks')
    
    def setSupportMultilineTasks(self, supportMultilineTasks):
        self._setData('support_multiline_tasks', supportMultilineTasks)
    
    def setViewHeight(self,height):
        self._setData('view_size_height', height)

    def setViewWidth(self,width):
        self._setData('view_size_width', width)

    def getViewHeight(self):
        return self._getData('view_size_height')

    def getViewWidth(self):
        return self._getData('view_size_width')

    def setViewPositionX(self,x):
        self._setData('view_position_x', x)

    def setViewPositionY(self,y):
        self._setData('view_position_y', y)

    def getViewPositionX(self):
        return self._getData('view_position_x')

    def getViewPositionY(self):
        return self._getData('view_position_y')

    def setEditViewHeight(self,height):
        self._setData('editview_size_height', height)
    
    def setEditViewWidth(self,width):
        self._setData('editview_size_width', width)

    def getEditViewHeight(self):
        return self._getData('editview_size_height')
    
    def getEditViewWidth(self):
        return self._getData('editview_size_width')
    
    def setViewSlidderPosition(self,position):
        self._setData('view_slidder_position', position)

    def getViewSlidderPosition(self):
        return self._getData('view_slidder_position')

    def _getData(self, key):
        if self._data:
            return self._data.get(key)
        return None

    def _setData(self, key, value):
        if not self._data:
            self._data = dict()
        self._data[key] = value
        self._save()

    def _save(self):
        if self._data:
            with open(self._file, 'tw') as file:
                json.dump(self._data, file, indent=4, sort_keys=True)
