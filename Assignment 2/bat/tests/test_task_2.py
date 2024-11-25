import unittest

from src.business_logic import can_borrow_carpentry_tool

'''
Possible tests:
Let A = (fees_owed > 0)
Let B = (patron_age <= 18)
Let C = (patron_age >= 90)
1: A=F, B=F, C=F, Outcome=F
2: A=F, B=F, C=T, Outcome=T
3: A=F, B=T, C=F, Outcome=T
4: A=T, B=F, C=F, Outcome=T
5: A=T, B=T, C=F, Outcome=T
6: A=T, B=F, C=T, Outcome=T
7: A=F, B=T, C=T, Outcome=T
8: A=T, B=T, C=T, Outcome=T

Optimal test sets:
- 1, 2, 3, 4
- 1, 2, 3, 5
- 1, 2, 4, 7
- 1, 3, 4, 6

Set chosen: 
The first set (1, 2, 3, 4)
'''

class TestCanBorrowCarpentryTool(unittest.TestCase):
    # Test for 1: A=F, B=F, C=F, Outcome=F
    def test_no_fees_adult_not_senior(self):
        self.assertTrue(can_borrow_carpentry_tool(30, 7, 0, True))

    # Test for 2: A=F, B=F, C=T, Outcome=T
    def test_no_fees_adult_senior(self):
        self.assertFalse(can_borrow_carpentry_tool(91, 7, 0, True))

    # Test for 3: A=F, B=T, C=F, Outcome=T
    def test_no_fees_minor_not_senior(self):
        self.assertFalse(can_borrow_carpentry_tool(17, 7, 0, True))

    # Test for 4: A=T, B=F, C=F, Outcome=T
    def test_fees_adult_not_senior(self):
        self.assertFalse(can_borrow_carpentry_tool(30, 7, 10, True))

    # # Additional test for length_of_loan > 14
    # def test_long_loan_period(self):
    #     self.assertFalse(can_borrow_carpentry_tool(30, 15, 0, True))

    # # Additional test for carpentry_tool_training = False
    # def test_no_training(self):
    #     self.assertFalse(can_borrow_carpentry_tool(30, 7, 0, False))

