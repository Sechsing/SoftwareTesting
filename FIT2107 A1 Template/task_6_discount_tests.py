'''
Unit tests for task 6 of assignment 1.

Reminder, the method you are testing is:
    calculate_discount(age)
Data types and descriptions are provided in the assignment specification.

You can assume that the calculate_discount method is already imported into this python module,
so you can call "calculate_discount" directly.

Author: Chua Sheng Xin
Student ID: 32837933
'''
import unittest

class TestCalculateDiscount(unittest.TestCase):
    # Equivalence Partitioning
    def test_error(self):
        self.assertEqual(calculate_discount(-1), "ERROR")   # Invalid partition: Negative age
        self.assertEqual(calculate_discount(121), "ERROR")  # Invalid partition: Extremely high age

    # Equivalence Partitioning & Boundary Value Analysis
    def test_0_discount(self):
        # Boundary Value Analysis
        self.assertEqual(calculate_discount(0), 0)          # Lower boundary
        self.assertEqual(calculate_discount(1), 0)          # Close to boundary
        self.assertEqual(calculate_discount(50), 0)         # Upper boundary of 0% discount
        # Equivalence Partitioning
        self.assertEqual(calculate_discount(25), 0)         # Representative of 0% discount 

    # Equivalence Partitioning & Boundary Value Analysis
    def test_10_discount(self):
        # Boundary Value Analysis
        self.assertEqual(calculate_discount(51), 10)        # Lower boundary of 10% discount
        self.assertEqual(calculate_discount(52), 10)        # Close to boundary of 10% discount
        self.assertEqual(calculate_discount(64), 10)        # Upper boundary of 10% discount
        # Equivalence Partitioning
        self.assertEqual(calculate_discount(57), 10)        # Representative of 10% discount 

    # Equivalence Partitioning & Boundary Value Analysis
    def test_15_discount(self):
        # Boundary Value Analysis
        self.assertEqual(calculate_discount(65), 15)        # Lower boundary of 15% discount
        self.assertEqual(calculate_discount(66), 15)        # Close to boundary of 15% discount
        self.assertEqual(calculate_discount(89), 15)        # Upper boundary of 15% discount
        # Equivalence Partitioning
        self.assertEqual(calculate_discount(77), 15)        # Representative of 15% discount

    # Equivalence Partitioning & Boundary Value Analysis
    def test_100_discount(self):
        # Boundary Value Analysis
        self.assertEqual(calculate_discount(90), 100)       # Lower boundary of 100% discount
        self.assertEqual(calculate_discount(91), 100)       # Close to boundary of 100% discount
        self.assertEqual(calculate_discount(120), 100)      # Upper boundary of 100% discount
        # Equivalence Partitioning
        self.assertEqual(calculate_discount(105), 100)      # Representative of 100% discount 