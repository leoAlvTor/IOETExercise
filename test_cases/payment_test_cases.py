import unittest
from controller.payment import Payment


class PaymentTestCase(unittest.TestCase):

    payment_object = Payment('RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00')

    def test_week_time_hours(self):
        # Test if week_time_hours dictionary is equal to the next dictionary:
        week_time_hours: dict = {
            '00:01-09:00': [0, 9],
            '09:01-18:00': [9, 18],
            '18:01-00:00': [18, 24]
        }
        self.assertDictEqual(self.payment_object.week_time_hours, week_time_hours, 'Week-Hours dict does not match!')

    def test_get_worked_days(self):
        # Test case for 5 records
        self.assertEqual(len(self.payment_object.get_worked_days('MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,'
                                                                 'SA14:00-18:00,SU20:00-21:00')), 5)
        # Test case for 2 records
        self.assertEqual(len(self.payment_object.get_worked_days('MO10:00-12:00,SA11:00-12:00')), 2)
        # Test case for 2 records (3 entries, one entry does not meet the pattern)
        self.assertEqual(len(self.payment_object.get_worked_days('MO10:00-12:00,SA11:00-12:00,DO00:00.11:00')), 2)
        # Test case for 0 records (1 entry, but does not meet the pattern)
        self.assertEqual(len(self.payment_object.get_worked_days('dummy_entry')), 0)

    def test_get_hours_from_string(self):
        self.assertTupleEqual(self.payment_object.get_hours_from_string(['08:00', '10:00']), (8, 10))
        self.assertTupleEqual(self.payment_object.get_hours_from_string(['09:00', '12:00']), (9, 12))
        self.assertTupleEqual(self.payment_object.get_hours_from_string(['01:00', '04:00']), (1, 4))
        # Test case when the hour is not right.
        with self.assertRaises(Exception) as context:
            self.payment_object.get_hours_from_string(['XX:00', "20:00"])
        self.assertTrue('Error while parsing the string:' in str(context.exception))
        # Test case when the hour is out of range.
        with self.assertRaises(Exception) as context:
            self.payment_object.get_hours_from_string(['10:00', "24:00"])
        self.assertTrue('Error while parsing the string:' in str(context.exception))

    def test_check_days_validity(self):
        # Test case for monday
        self.assertEqual(self.payment_object.check_days_validity('MO'), True)
        # Test case for saturday
        self.assertEqual(self.payment_object.check_days_validity('SA'), True)
        # Test case for sunday
        self.assertEqual(self.payment_object.check_days_validity('SU'), True)
        # Test case when day is not right.
        self.assertEqual(self.payment_object.check_days_validity('DE'), False)
        # Test case when day is not right.
        self.assertEqual(self.payment_object.check_days_validity('JA'), False)

    def test_check_hours_validity(self):
        # Shifts the end_time to 24
        self.assertTupleEqual(self.payment_object.check_hours_validity(start_end_pair=[0, 9], end_time=0),
                              ([0, 9], 24))
        # Keeps the same values
        self.assertTupleEqual(self.payment_object.check_hours_validity(start_end_pair=[9, 18], end_time=24),
                              ([9, 18], 24))
        # Shifts the end_time from start_end_pair to 24 and end_time to 24
        self.assertTupleEqual(self.payment_object.check_hours_validity(start_end_pair=[18, 0], end_time=0),
                              ([18, 24], 24))
        # Keeps the same values
        self.assertTupleEqual(self.payment_object.check_hours_validity(start_end_pair=[0, 9], end_time=1),
                              ([0, 9], 1))
        # Shifts the end_time from start_end_pair to 24
        self.assertTupleEqual(self.payment_object.check_hours_validity(start_end_pair=[0, 0], end_time=10),
                              ([0, 24], 10))

    def test_calculate_hour_price(self):
        # Please refer to 'ACME.txt' file

        # Test case for Mario, cumulative value is = 320
        self.assertEqual(self.payment_object.calculate_salary_per_hours(day='TU', start_time=8, end_time=18),
                         float(160))
        self.assertEqual(self.payment_object.calculate_salary_per_hours(day='SU', start_time=10, end_time=18),
                         float(160))

        # Test case for Zoila:
        # Special case, as the start_hour and end_hour are the same the return value will be equal to zero!
        self.assertNotEqual(self.payment_object.calculate_salary_per_hours(day='SA', start_time=18, end_time=18),
                            float(625))
        # Special case, as the start_hour is greater than the end time it should be split:
        # 1. start_time=12 end_time=24
        # 2. start_time=00 end_time=11
        self.assertNotEqual(self.payment_object.calculate_salary_per_hours(day='SU', start_time=12, end_time=11),
                            float(525))

    def test_get_next_day(self):
        # Normal test
        self.assertEqual(self.payment_object.get_next_day('MO'), 'TU')
        # First day of the weekend
        self.assertEqual(self.payment_object.get_next_day('FR'), 'SA')
        # Shifts SAturday to SUnday
        self.assertEqual(self.payment_object.get_next_day('SA'), 'SU')
        # Last day of the weekend
        self.assertEqual(self.payment_object.get_next_day('SU'), 'MO')

    def test_calculate_whole_day(self):
        # Special case
        # Whole weekend salary = $600
        self.assertEqual(self.payment_object.calculate_whole_day(is_weekend=True, day='SA', start_hour=0, end_hour=0),
                         600)
        # Special case
        # Sunday start hour 12:00 end hour 24:00 = $270
        # Monday start hour 00:00 end hour 12:00 = $270
        self.assertEqual(self.payment_object.calculate_whole_day(is_weekend=True, day='SU', start_hour=12, end_hour=12),
                         540)
        # Special case
        # Sunday start hour 12:00 end hour 24:00 = $270
        # Monday start hour 00:00 end hour 11:00 = $255
        self.assertEqual(self.payment_object.calculate_whole_day(is_weekend=False, day='SU', start_hour=12, end_hour=11),
                         525)

    def test_calculate_salary(self):
        # LEO
        # NORMAL TEST CASE
        self.assertEqual(self.payment_object.calculate_salary(['MO08:00-10:00', 'TU08:00-10:00', 'TH01:00-04:00',
                                                               'SA12:00-16:00']), float(235))
        # MARIO
        # NORMAL TEST CASE
        self.assertEqual(self.payment_object.calculate_salary(['TU08:00-18:00', 'SU10:00-18:00']),
                         float(320))
        # GRACIELA
        # SPECIAL TEST CASE
        # ** Tuesday starts at 10:00 and ends Wednesday at 01:00
        self.assertEqual(self.payment_object.calculate_salary(['TU10:00-01:00', 'TH05:00-10:00', 'FR18:00-20:00']),
                         float(420))
        # MIGUEL
        # NORMAL TEST CASE
        self.assertEqual(self.payment_object.calculate_salary(['FR08:00-21:00']),
                         float(220))
        # MARIELA
        # SPECIAL TEST CASE
        # ** Friday starts at 12:00 and ends Saturday at 12:00
        self.assertEqual(self.payment_object.calculate_salary(['FR12:00-12:00']),
                         float(540))
        # RAMON
        # SPECIAL TEST CASE
        # ** Saturday whole day (600).
        # ** Sunday starts at 12:00 and ends Monday at 12:00
        self.assertEqual(self.payment_object.calculate_salary(['SA18:00-18:00', 'SU12:00-12:00']),
                         float(1140))

    def test_get_output(self):
        self.assertEqual(self.payment_object.get_output(215), 'The amount to pay RENE is: 215 USD')


if __name__ == '__main__':
    unittest.main()
