"""This is a small test file to check if the data is parsed correctly"""
import unittest
from constants import STUDENTS_PATH, SEMESTERS
import pandas as pd


class TestStudentsData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.students = pd.read_excel(STUDENTS_PATH,
                                     sheet_name='Sheet1',
                                     index_col=[0, 1, 2],
                                     header=[0, 2],)
        cls.students.index = cls.students.index.droplevel(0)

    def helper_test_students(self, subject, category, year, test_cases):
        for semester, expected_count in zip(SEMESTERS, test_cases):
            with self.subTest(semester=semester):
                actual_count = self.students.loc[(subject, category), (year, semester)]
                self.assertEqual(actual_count, expected_count)

    def test_student_counts_HF(self):
        test_cases = [0, 4, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 3]
        self.helper_test_students('"Englische Sprache und Literatur des Mittelalters"', 'HF', 'WiSe 2005/2006', test_cases)

    def test_student_counts_NF_1(self):
        test_cases = [0, 6, 1, 0, 0, 1, 1, 1, 0, 2, 0, 0, 0, 0]
        self.helper_test_students('"Englische Sprache und Literatur des Mittelalters"', 'NF', 'WiSe 2005/2006', test_cases)

    def test_student_counts_HF_2(self):
        test_cases = [0, 8, 5, 6, 1, 4, 1, 2, 2, 0, 3, 1, 1, 1]
        self.helper_test_students('"Südslavische Philologie"', 'HF', 'WiSe 2005/2006', test_cases)

    def test_student_counts_NF_2(self):
        test_cases = [0, 5, 3, 4, 0, 2, 0, 1, 2, 0, 0, 2, 0, 1]
        self.helper_test_students('"Südslavische Philologie"', 'NF', 'WiSe 2005/2006', test_cases)

    def test_student_counts_HF_3(self):
        test_cases = [0, 132, 7, 91, 15, 75, 18, 69, 9, 84, 15, 93, 8, 97]
        self.helper_test_students('"Informatik"', 'HF', 'WiSe 2005/2006', test_cases)

    def test_student_counts_NF_3(self):
        test_cases = [0, 18, 0, 11, 5, 5, 2, 6, 1, 2, 1, 2, 2, 5]
        self.helper_test_students('"Informatik"', 'NF', 'WiSe 2005/2006', test_cases)

    def test_student_counts_HF_4(self):
        test_cases = [0, 0, 0, 4, 7, 0, 2, 2, 1, 0, 0, 1, 0, 0]
        self.helper_test_students('"Deutsche Literaturgeschichte"', 'HF', 'SoSe 2013', test_cases)

    def test_student_counts_NF_4(self):
        test_cases = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.helper_test_students('"Deutsche Literaturgeschichte"', 'NF', 'SoSe 2013', test_cases)

    def test_student_counts_HF_5(self):
        test_cases = [0, 5, 0, 4, 0, 6, 0, 2, 0, 0, 0, 0, 0, 0]
        self.helper_test_students('"Archäologie des Mittelalters und der Neuzeit"', 'HF', 'WiSe 2023/2024', test_cases)

    def test_student_counts_NF_5(self):
        test_cases = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.helper_test_students('"Archäologie des Mittelalters und der Neuzeit"', 'NF', 'WiSe 2023/2024', test_cases)


if __name__ == '__main__':
    unittest.main()
