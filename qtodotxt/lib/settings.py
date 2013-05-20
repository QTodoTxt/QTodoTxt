import os
import pickle

DEFAULT_SETTINGS_FILE = os.path.expanduser("~/.qtodotxt.cfg")

class Settings(object):
    def __init__(self):
        self._file = DEFAULT_SETTINGS_FILE
        self._data = dict()
            
    def load(self, filename=DEFAULT_SETTINGS_FILE):
        self._file = filename
        if os.path.exists(self._file):
            with open(self._file) as file:
                self._data = pickle.load(file)
            
    def getLastOpenFile(self):
        return self._getData('last_open_file')
    
    def setLastOpenFile(self, last_open_file):
        self._setData('last_open_file', last_open_file)

    def _getData(self, key):
        if self._data:
            return self._data['last_open_file']
        return None

    def _setData(self, key, value):
        if not self._data:
            self._data = dict()
        self._data[key] = value
        self._save()
    
    def _save(self):
        if self._data:
            with open(self._file, 'w') as file:
                file = open(self._file, 'w') 
                pickle.dump(self._data, file)
    