import json
import unittest
from tempfile import mkstemp
from os import remove
from qtodotxt.lib.settings import Settings


class TestSettingsLoadSave(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file = mkstemp(text=True)[1]
        with open(cls.file, 'tw') as f:
            json.dump({}, f)
        cls.SAMPLE_FILENAME = 'todo.txt'

    @classmethod
    def tearDownClass(cls):
        remove(cls.file)

    def test_00_save(self):
        setting1 = Settings()
        setting1.load(self.file)
        setting1.setLastOpenFile(self.SAMPLE_FILENAME)

    def test_01_load(self):
        setting2 = Settings()
        setting2.load(self.file)
        self.assertEqual(setting2.getLastOpenFile(), self.SAMPLE_FILENAME)
