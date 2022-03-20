import unittest
from utilities.file_utility import FileUtility


class MyTestCase(unittest.TestCase):

    # Please, change the path!
    file_utility = FileUtility('/home/leo/PycharmProjects/IOETExercise/ACME payment.txt')

    def test_check_file_exists(self):
        self.assertEqual(self.file_utility.check_file_exists(), True)

    def test_read_file(self):
        self.assertEqual(len(self.file_utility.read_file()), 11)

    def test_check_entries_integrity(self):
        test_entries = ['RAMON=SA18:00-18:00,SU12:00-12:00',
                        'ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00',
                        'FR08:00-21:00']
        self.assertEqual(len(self.file_utility.check_entries_integrity(test_entries)), 2)


if __name__ == '__main__':
    unittest.main()
