import unittest
from unittest import mock
from src.bat_ui import BatUI


class TestMainMenu(unittest.TestCase):
    """Test suite for the Main Menu functionality of BatUI."""

    def setUp(self):
        """Set up common test variables."""
        # Mock the data_manager with necessary attributes and methods
        self.data_manager_mock = mock.Mock()
        # Initialize patron_data and catalogue_data as needed
        self.data_manager_mock._patron_data = []
        self.data_manager_mock._catalogue_data = []
        self.ui = BatUI(self.data_manager_mock)

    # Loan Item Tests
    @mock.patch('src.bat_ui.logic.process_loan')
    @mock.patch('src.bat_ui.search.find_patron_by_name_and_age')
    @mock.patch('src.bat_ui.search.find_item_by_id')
    @mock.patch('src.bat_ui.user_input.read_bool')
    @mock.patch('src.bat_ui.user_input.read_string')
    @mock.patch('src.bat_ui.user_input.read_integer')
    def test_loan_item_successful_loan(self, mock_read_integer, mock_read_string, mock_read_bool,
                                      mock_find_item_by_id, mock_find_patron_by_name_and_age,
                                      mock_process_loan):
        """Test successful loan process."""
        # Arrange
        # Simulate entering the loan item screen
        self.ui._current_screen = self.ui._loan_item

        # Set up mocks for _loan_item
        mock_read_integer.side_effect = [1, 30, 7]  # item_id, patron age, loan length
        mock_find_item_by_id.return_value = mock.Mock(_type='Hammer', _name='Heavy Hammer', _year=2020, _id=1)
        mock_read_bool.return_value = 'y'
        mock_read_string.return_value = 'John Doe'
        patron_mock = mock.Mock(_name='John Doe', _age=30, _loans=[], _outstanding_fees=0, _makerspace_training=True)
        mock_find_patron_by_name_and_age.return_value = patron_mock
        mock_process_loan.return_value = True

        # Act
        self.ui.run_current_screen()

        # Assert
        self.assertEqual(
            self.ui.get_current_screen(),
            "MAIN MENU",
            "After successful loan, should return to MAIN MENU."
        )
        mock_process_loan.assert_called_once_with(patron_mock, mock_find_item_by_id.return_value, 7)

    @mock.patch('src.bat_ui.logic.process_loan')
    @mock.patch('src.bat_ui.search.find_patron_by_name_and_age')
    @mock.patch('src.bat_ui.search.find_item_by_id')
    @mock.patch('src.bat_ui.user_input.read_bool')
    @mock.patch('src.bat_ui.user_input.read_string')
    @mock.patch('src.bat_ui.user_input.read_integer')
    def test_loan_item_no_such_item(self, mock_read_integer, mock_read_string, mock_read_bool,
                                   mock_find_item_by_id, mock_find_patron_by_name_and_age,
                                   mock_process_loan):
        """Test loaning an item that does not exist."""
        # Arrange
        # Simulate entering the loan item screen
        self.ui._current_screen = self.ui._loan_item

        # Set up mocks for _loan_item
        mock_read_integer.return_value = 999  # Non-existent item ID
        mock_find_item_by_id.return_value = None  # Item not found

        # Act
        self.ui.run_current_screen()

        # Assert
        self.assertEqual(
            self.ui.get_current_screen(),
            "MAIN MENU",
            "After attempting to loan non-existent item, should return to MAIN MENU."
        )
        mock_process_loan.assert_not_called()

    @mock.patch('src.bat_ui.logic.process_loan')
    @mock.patch('src.bat_ui.search.find_patron_by_name_and_age')
    @mock.patch('src.bat_ui.search.find_item_by_id')
    @mock.patch('src.bat_ui.user_input.read_bool')
    @mock.patch('src.bat_ui.user_input.read_string')
    @mock.patch('src.bat_ui.user_input.read_integer')
    def test_loan_item_no_such_patron(self, mock_read_integer, mock_read_string, mock_read_bool,
                                     mock_find_item_by_id, mock_find_patron_by_name_and_age,
                                     mock_process_loan):
        """Test loaning an item to a patron that does not exist."""
        # Arrange
        # Simulate entering the loan item screen
        self.ui._current_screen = self.ui._loan_item

        # Set up mocks for _loan_item
        mock_read_integer.side_effect = [1, 40]  # item_id, patron age
        mock_find_item_by_id.return_value = mock.Mock(_type='Drill', _name='Power Drill', _year=2021, _id=1)
        mock_read_bool.return_value = 'y'
        mock_read_string.return_value = 'Non Existent'
        mock_find_patron_by_name_and_age.return_value = None  # Patron not found

        # Act
        self.ui.run_current_screen()

        # Assert
        self.assertEqual(
            self.ui.get_current_screen(),
            "MAIN MENU",
            "After attempting to loan to non-existent patron, should return to MAIN MENU."
        )
        mock_process_loan.assert_not_called()

    @mock.patch('src.bat_ui.logic.process_loan')
    @mock.patch('src.bat_ui.search.find_patron_by_name_and_age')
    @mock.patch('src.bat_ui.search.find_item_by_id')
    @mock.patch('src.bat_ui.user_input.read_bool')
    @mock.patch('src.bat_ui.user_input.read_string')
    @mock.patch('src.bat_ui.user_input.read_integer')
    def test_loan_item_patron_cannot_borrow(self, mock_read_integer, mock_read_string, mock_read_bool,
                                           mock_find_item_by_id, mock_find_patron_by_name_and_age,
                                           mock_process_loan):
        """Test loaning an item when the patron is not allowed to borrow."""
        # Arrange
        # Simulate entering the loan item screen
        self.ui._current_screen = self.ui._loan_item

        # Set up mocks for _loan_item
        mock_read_integer.side_effect = [2, 50, 7]  # item_id, patron age, loan length
        mock_find_item_by_id.return_value = mock.Mock(_type='Saw', _name='Circular Saw', _year=2019, _id=2)
        mock_read_bool.return_value = 'y'
        mock_read_string.return_value = 'Restricted Patron'
        patron_mock = mock.Mock(_name='Restricted Patron', _age=50, _loans=[], _outstanding_fees=100, _makerspace_training=False)
        mock_find_patron_by_name_and_age.return_value = patron_mock
        mock_process_loan.return_value = False  # Patron cannot borrow

        # Act
        self.ui.run_current_screen()

        # Assert
        self.assertEqual(
            self.ui.get_current_screen(),
            "MAIN MENU",
            "After failed loan, should return to MAIN MENU."
        )
        mock_process_loan.assert_called_once_with(patron_mock, mock_find_item_by_id.return_value, 7)

    @mock.patch('src.bat_ui.search.find_patron_by_name_and_age')
    @mock.patch('src.bat_ui.search.find_item_by_id')
    @mock.patch('src.bat_ui.user_input.read_bool')
    @mock.patch('src.bat_ui.user_input.read_string')
    @mock.patch('src.bat_ui.user_input.read_integer')
    def test_loan_item_cancelled_by_user(self, mock_read_integer, mock_read_string, mock_read_bool,
                                        mock_find_item_by_id, mock_find_patron_by_name_and_age):
        """Test loaning an item where the user cancels the operation."""
        # Arrange
        # Simulate entering the loan item screen
        self.ui._current_screen = self.ui._loan_item

        # Set up mocks for _loan_item
        mock_read_integer.return_value = 1  # item_id
        mock_find_item_by_id.return_value = mock.Mock(_type='Hammer', _name='Heavy Hammer', _year=2020, _id=1)
        mock_read_bool.return_value = 'n'  # User cancels
        mock_read_string.return_value = 'John Doe'  # Should not be used

        # Act
        self.ui.run_current_screen()

        # Assert
        mock_find_item_by_id.assert_called_once_with(1, self.data_manager_mock._catalogue_data)
        mock_find_patron_by_name_and_age.assert_not_called()
        self.assertEqual(
            self.ui.get_current_screen(),
            "MAIN MENU",
            "After user cancels loan, should return to MAIN MENU."
        )

    # Return Item Tests
    @mock.patch('src.bat_ui.logic.process_return')
    @mock.patch('src.bat_ui.search.find_patron_by_name_and_age')
    @mock.patch('src.bat_ui.user_input.read_integer')
    @mock.patch('src.bat_ui.user_input.read_string')
    def test_return_item_successful_return(self, mock_read_string, mock_read_integer,
                                          mock_find_patron_by_name_and_age, mock_process_return):
        """Test successful return of an item."""
        # Arrange
        patron_mock = mock.Mock(_name='Jane Smith', _age=25, _loans=[
            mock.Mock(_item=mock.Mock(_id=10, _name='Book A'), __str__=mock.Mock(return_value='10: Book A'))
        ])
        mock_find_patron_by_name_and_age.return_value = patron_mock
        mock_read_string.return_value = 'Jane Smith'
        mock_read_integer.side_effect = [25, 10]  # Patron age, Item ID to return

        # Simulate entering the return item screen
        self.ui._current_screen = self.ui._return_item

        # Act
        self.ui.run_current_screen()

        # Assert
        mock_find_patron_by_name_and_age.assert_called_once_with('Jane Smith', 25, self.data_manager_mock._patron_data)
        mock_process_return.assert_called_once_with(patron_mock, 10)
        self.assertEqual(
            self.ui.get_current_screen(),
            "MAIN MENU",
            "After successful return, should return to MAIN MENU."
        )

    @mock.patch('src.bat_ui.search.find_patron_by_name_and_age')
    @mock.patch('src.bat_ui.user_input.read_integer')
    @mock.patch('src.bat_ui.user_input.read_string')
    def test_return_item_no_such_patron(self, mock_read_string, mock_read_integer,
                                       mock_find_patron_by_name_and_age):
        """Test returning an item for a patron that does not exist."""
        # Arrange
        mock_find_patron_by_name_and_age.return_value = None
        mock_read_string.return_value = 'Nonexistent Patron'
        mock_read_integer.side_effect = [40]  # Patron age

        # Simulate entering the return item screen
        self.ui._current_screen = self.ui._return_item

        # Act
        self.ui.run_current_screen()

        # Assert
        mock_find_patron_by_name_and_age.assert_called_once_with('Nonexistent Patron', 40, self.data_manager_mock._patron_data)
        self.assertEqual(
            self.ui.get_current_screen(),
            "MAIN MENU",
            "After attempting to return with non-existent patron, should return to MAIN MENU."
        )

    @mock.patch('src.bat_ui.search.find_patron_by_name_and_age')
    @mock.patch('src.bat_ui.user_input.read_integer')
    @mock.patch('src.bat_ui.user_input.read_string')
    @mock.patch('src.bat_ui.logic.process_return')
    def test_return_item_no_such_item(self, mock_process_return, mock_read_string, mock_read_integer,
                                     mock_find_patron_by_name_and_age):
        """Test returning an item that is not in the patron's loans."""
        # Arrange
        patron_mock = mock.Mock(_name='John Doe', _age=30, _loans=[
            mock.Mock(_item=mock.Mock(_id=20, _name='Drill'), __str__=mock.Mock(return_value='20: Drill'))
        ])
        mock_find_patron_by_name_and_age.return_value = patron_mock
        mock_read_string.return_value = 'John Doe'
        mock_read_integer.side_effect = [30, 999, 20]  # Patron age, Invalid Item ID, Valid Item ID

        # Simulate entering the return item screen
        self.ui._current_screen = self.ui._return_item

        # Act
        self.ui.run_current_screen()

        # Assert
        mock_find_patron_by_name_and_age.assert_called_once_with('John Doe', 30, self.data_manager_mock._patron_data)
        mock_process_return.assert_called_once_with(patron_mock, 20)
        self.assertEqual(
            self.ui.get_current_screen(),
            "MAIN MENU",
            "After attempting to return invalid item, should return to MAIN MENU."
        )

    # Register Patron Test ---
    @mock.patch('src.bat_ui.user_input.read_integer_range', return_value=25)
    @mock.patch('src.bat_ui.user_input.read_string', return_value='Jane Doe')
    def test_register_patron_successful(self, mock_read_string, mock_read_integer_range):
        """Test successful registration of a new patron."""
        # Arrange
        # Simulate entering the register patron screen
        self.ui._current_screen = self.ui._register_patron

        # Act
        self.ui.run_current_screen()

        # Assert
        self.data_manager_mock.register_patron.assert_called_once_with('Jane Doe', 25)
        self.assertEqual(
            self.ui.get_current_screen(),
            "MAIN MENU",
            "After registering patron, should return to MAIN MENU."
        )
