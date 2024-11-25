'''
Unit tests for task 6 of assignment 1.

Reminder, the method you are testing is:
    type_of_patron(age)
Data types and descriptions are provided in the assignment specification.

You can assume that the type_of_patron method is already imported into this python module,
so you can call "type_of_patron" directly.

Author: Chua Sheng Xin
Student ID: 32837933
'''
import unittest

class TestTypeOfPatron(unittest.TestCase):
    # Equivalence Partitioning
    def test_error(self):
        self.assertEqual(type_of_patron(-1), "ERROR")   # Invalid partition: Negative age
        self.assertEqual(type_of_patron(131), "ERROR")  # Invalid partition: Extremely high age

    # Equivalence Partitioning & Boundary Value Analysis
    def test_minor(self):
        # Boundary Value Analysis
        self.assertEqual(type_of_patron(0), "MINOR")    # Lower boundary of Minor
        self.assertEqual(type_of_patron(1), "MINOR")    # Close to boundary of Minor
        self.assertEqual(type_of_patron(17), "MINOR")   # Upper boundary of Minor
        # Equivalence Partitioning
        self.assertEqual(type_of_patron(9), "MINOR")    # Representative of Minor
    
    # Equivalence Partitioning & Boundary Value Analysis
    def test_adult(self):
        # Boundary Value Analysis
        self.assertEqual(type_of_patron(18), "ADULT")   # Lower boundary of Adult
        self.assertEqual(type_of_patron(19), "ADULT")   # Close to boundary of Adult
        self.assertEqual(type_of_patron(89), "ADULT")   # Upper boundary of Adult
        # Equivalence Partitioning
        self.assertEqual(type_of_patron(54), "ADULT")   # Representative of Adult

    # Equivalence Partitioning & Boundary Value Analysis
    def test_elderly(self):
        # Boundary Value Analysis
        self.assertEqual(type_of_patron(90), "ELDERLY")  # Lower boundary of Elderly
        self.assertEqual(type_of_patron(91), "ELDERLY")  # Close to boundary of Elderly
        self.assertEqual(type_of_patron(130), "ELDERLY") # Upper boundary of Elderly
        # Equivalence Partitioning
        self.assertEqual(type_of_patron(110), "ELDERLY") # Representative of Elderly