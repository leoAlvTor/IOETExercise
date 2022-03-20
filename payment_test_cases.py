import unittest
import wave

from payment import Payment


class MyTestCase(unittest.TestCase):

    payment_object = Payment('RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00')

    def test_open_file(self):
        self.assertEqual(len(Payment.open_file(file_name='ACME payment.txt')), 11, 'Number of lines should be 11!')

    def test_week_time_hours(self):
        week_time_hours: dict = {
            '00:01-09:00': [0, 9],
            '09:01-18:00': [9, 18],
            '18:01-00:00': [18, 24]
        }
        self.assertDictEqual(self.payment_object.week_time_hours, week_time_hours, 'Week-Hours dict does not match!')

    def test_get_worked_days(self):
        # Test case for Rene
        self.assertEqual(len(self.payment_object.get_worked_days()), 5, 'Worked days length is not correct!')

    def test_get_hours_from_string(self):
        # Mixed test case
        self.assertTupleEqual(self.payment_object.get_hours_from_string(['08:00', '10:00']), (8, 10))
        self.assertTupleEqual(self.payment_object.get_hours_from_string(['09:00', '12:00']), (9, 12))
        self.assertTupleEqual(self.payment_object.get_hours_from_string(['01:00', '04:00']), (1, 4))
        self.assertTupleEqual(self.payment_object.get_hours_from_string(['00:00', '14:00']), (0, 14))

    def test_check_hours_validity(self):
        # Mixed test case
        self.assertTupleEqual(self.payment_object.check_hours_validity(start_end_pair=[0, 9], end_time=0),
                              ([0, 9], 24))
        self.assertTupleEqual(self.payment_object.check_hours_validity(start_end_pair=[9, 18], end_time=24),
                              ([9, 18], 24))
        self.assertTupleEqual(self.payment_object.check_hours_validity(start_end_pair=[18, 0], end_time=0),
                              ([18, 24], 24))
        self.assertTupleEqual(self.payment_object.check_hours_validity(start_end_pair=[0, 9], end_time=1),
                              ([0, 9], 1))
        self.assertTupleEqual(self.payment_object.check_hours_validity(start_end_pair=[0, 9], end_time=10),
                              ([0, 9], 10))
        self.assertTupleEqual(self.payment_object.check_hours_validity(start_end_pair=[9, 18], end_time=10),
                              ([9, 18], 10))

    def test_calculate_hour_price(self):
        # Test case for mario
        self.assertEqual(self.payment_object.calculate_salary_per_hours('TU', 8, 18), float(160))
        self.assertEqual(self.payment_object.calculate_salary_per_hours('SU', 10, 18), float(160))

    def test_get_next_day(self):
        # Normal test
        self.assertEqual(self.payment_object.get_next_day('MO'), 'TU')
        # First day of the weekend
        self.assertEqual(self.payment_object.get_next_day('FR'), 'SA')
        # Last day of the weekend
        self.assertEqual(self.payment_object.get_next_day('SU'), 'MO')

    def test_calculate_salary(self):
        # LEO
        self.assertEqual(self.payment_object.calculate_salary(['MO08:00-10:00', 'TU08:00-10:00', 'TH01:00-04:00',
                                                               'SA12:00-16:00']), float(235))

        # MARIO
        self.assertEqual(self.payment_object.calculate_salary(['TU08:00-18:00', 'SU10:00-18:00']),
                         float(320))

        # GRACIELA
        self.assertEqual(self.payment_object.calculate_salary(['TU10:00-01:00', 'TH05:00-10:00', 'FR18:00-20:00']),
                         float(420))

    def test_get_output(self):
        self.assertEqual(self.payment_object.get_output(155), 'The amount to pay Temporal_User is: 155 USD')


if __name__ == '__main__':
    unittest.main()
