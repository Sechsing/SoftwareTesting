import unittest

from unittest.mock import patch
from src.bat_ui import BatUI
from src.data_mgmt import DataManager

class TestMainMenu(unittest.TestCase):

    def setUp(self):
        """Set up a fresh instance of the BatUI with a mock DataManager before each test."""
        self.data_manager = DataManager()  # Mocked data manager for the tests
        self.ui = BatUI(self.data_manager)

    @patch('src.user_input.read_integer_range')
    def test_valid_input_loan_item(self, mock_input):
        """Test valid input '1' leads to Loan Item screen."""
        mock_input.return_value = 1
        self.ui.run_current_screen()
        self.assertEqual(self.ui.get_current_screen(), "LOAN ITEM")

    @patch('src.user_input.read_integer_range')
    def test_valid_input_return_item(self, mock_input):
        """Test valid input '2' leads to Return Item screen."""
        mock_input.return_value = 2
        self.ui.run_current_screen()
        self.assertEqual(self.ui.get_current_screen(), "RETURN ITEM")

    @patch('src.user_input.read_integer_range')
    def test_valid_input_search_for_patron(self, mock_input):
        """Test valid input '3' leads to Search for Patron screen."""
        mock_input.return_value = 3
        self.ui.run_current_screen()
        self.assertEqual(self.ui.get_current_screen(), "SEARCH FOR PATRON")

    @patch('src.user_input.read_integer_range')
    def test_valid_input_register_patron(self, mock_input):
        """Test valid input '4' leads to Register Patron screen."""
        mock_input.return_value = 4
        self.ui.run_current_screen()
        self.assertEqual(self.ui.get_current_screen(), "REGISTER PATRON")

    @patch('src.user_input.read_integer_range')
    def test_valid_input_access_makerspace(self, mock_input):
        """Test valid input '5' leads to Access Makerspace screen."""
        mock_input.return_value = 5
        self.ui.run_current_screen()
        self.assertEqual(self.ui.get_current_screen(), "ACCESS MAKERSPACE")

    @patch('src.user_input.read_integer_range')
    def test_valid_input_quit(self, mock_input):
        """Test valid input '6' leads to Quit screen."""
        mock_input.return_value = 6
        self.ui.run_current_screen()
        self.assertEqual(self.ui.get_current_screen(), "QUIT")

    @patch('src.user_input.read_integer_range')
    def test_invalid_input_retries(self, mock_input):
        """Test invalid input is retried until a valid input is given."""
        # Simulate invalid input first, then valid input
        mock_input.side_effect = [7, 2]  # Invalid first, then valid

        # Call run_current_screen twice to simulate retrying after invalid input
        self.ui.run_current_screen()  # First run, invalid input (7) keeps us on the main menu
        self.ui.run_current_screen()  # Second run, valid input (2) should move us to RETURN ITEM

        # Should end up on Return Item screen after invalid input retry
        self.assertEqual(self.ui.get_current_screen(), "RETURN ITEM")



