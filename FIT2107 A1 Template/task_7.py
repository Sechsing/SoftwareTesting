'''
Unit tests for task 7 of assignment 1.

Reminder, the method you are testing is:
    can_borrow(item_type, patron_age, outstanding_fees, gardening_training, carpentry_training)
Data types and descriptions are provided in the assignment specification.

You can assume that the can_borrow method is already imported into this python module,
so you can call "can_borrow" directly.

Author:
Student ID:
'''
import unittest

class TestCanBorrow(unittest.TestCase):
    def test_can_borrow(self):
        # Test case 1
        self.assertEqual(can_borrow("gardening", 17, 5.0, True, False), False)
        # Test case 2
        self.assertEqual(can_borrow("carpentry", 17, 0, False, True), False)
        # Test case 3
        self.assertEqual(can_borrow("book", 90, 5.0, True, True), False)
        # Test case 4
        self.assertEqual(can_borrow("book", 50, 0, False, False), True)
        # Test case 5
        self.assertEqual(can_borrow("book", 90, 0, True, False), True)
        # Test case 6
        self.assertEqual(can_borrow("gardening", 50, 5.0, False, True), False)
        # Test case 7
        self.assertEqual(can_borrow("gardening", 90, 0, False, True), False)
        # Test case 8
        self.assertEqual(can_borrow("book", 90, 0, True, True), True)
        # Test case 9
        self.assertEqual(can_borrow("gardening", 17, 0, True, True), True)
        # Test case 10
        self.assertEqual(can_borrow("carpentry", 90, 5.0, True, False), False)
        # Test case 11
        self.assertEqual(can_borrow("carpentry", 50, 5.0, True, False), False)
        # Test case 12
        self.assertEqual(can_borrow("carpentry", 17, 5.0, False, False), False)
        # Test case 13
        self.assertEqual(can_borrow("book", 17, 0, True, True), True)