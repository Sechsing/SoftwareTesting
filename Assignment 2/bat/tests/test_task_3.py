import unittest

from src.business_logic import can_use_makerspace


'''
Feasible paths:
1: 135->148->150->151->153->154->161->164
2: 135->148->150->151->153->155->156->161->164
3: 135->148->150->151->153->155->157->158->159->161->162->164
4: 135->148->150->151->153->155->157->158->159->161->164
'''

class TestCanUseMakerspace(unittest.TestCase):
    # Path 1: Adult with completed training, no fees
    def test_adult_with_training_no_fees(self):
        # Expected: True as the patron is an adult with training and has no fees
        self.assertEqual(True, can_use_makerspace(25, 0, True))

    # Path 2: Adult with completed training and outstanding fees is not 0
    def test_adult_with_training_fees(self):
        # Expected: False as the patron is an adult with training but have outstanding fees
        self.assertEqual(False, can_use_makerspace(25, 100, True))

    # Path 3: Adult with no training and have outstanding fees
    def test_adult_no_training_with_fees(self):
        # Expected: False as the patron is an adult but has not completed training
        self.assertEqual(False, can_use_makerspace(25, 50, False))

    # Path 4: Adult with no training and no outstanding fees
    def test_adult_no_training_no_fees(self):
        # Expected: False as the patron is an adult and have no outstanding fees but has not completed training
        self.assertEqual(False, can_use_makerspace(25, 0, False))