import os
import pickle

DEFAULT_SETTINGS_FILE = os.path.expanduser("~/.qtodotxt.cfg")


class Settings(object):
    def __init__(self):
        self._file = DEFAULT_SETTINGS_FILE
        self._data = {}

    def load(self, filename=DEFAULT_SETTINGS_FILE):
        self._file = filename
        if os.path.exists(self._file):
            with open(self._file, 'br') as file:
                self._data = pickle.load(file)

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
            with open(self._file, 'bw') as file:
                pickle.dump(self._data, file)
