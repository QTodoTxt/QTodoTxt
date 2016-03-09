
import unittest
from datetime import date

from qtodotxt.ui.dialogs.taskeditor_dialog import end_of_month,  end_of_year, end_of_next_month
from qtodotxt.ui.dialogs.taskeditor_dialog import end_of_week, end_of_next_week


class TestDates(unittest.TestCase):

    def test_dates(self):
        self.assertEqual("2016-03-06", end_of_week(date(year=2016, month=3, day=5)))
        self.assertEqual("2016-03-06", end_of_week(date(year=2016, month=3, day=1)))
        self.assertEqual("2016-01-03", end_of_week(date(year=2015, month=12, day=31)))
        self.assertEqual("2016-03-13", end_of_next_week(date(year=2016, month=3, day=1)))

        self.assertEqual("2016-02-29", end_of_month(date(year=2016, month=2, day=5)))
        self.assertEqual("2016-02-29", end_of_next_month(date(year=2016, month=1, day=5)))
        self.assertEqual("2015-12-31", end_of_month(date(year=2015, month=12, day=31)))
        self.assertEqual("2016-01-31", end_of_next_month(date(year=2015, month=12, day=31)))

        self.assertEqual("2016-12-31", end_of_month(date(year=2016, month=12, day=5)))
        self.assertEqual("2017-01-31", end_of_next_month(date(year=2016, month=12, day=5)))

        self.assertEqual("2016-12-31", end_of_year(date(year=2016, month=1, day=5)))
