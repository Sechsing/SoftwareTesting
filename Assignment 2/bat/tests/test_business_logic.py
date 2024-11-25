import unittest

from unittest import mock
from datetime import date, timedelta
from src.business_logic import (
    type_of_patron,
    calculate_discount,
    can_borrow,
    can_borrow_book,
    can_borrow_gardening_tool,
    can_borrow_carpentry_tool,
    can_use_makerspace,
    process_loan,
    process_return
)
from src.patron import Patron
from src.borrowable_item import BorrowableItem
from src.loan import Loan

class TestBusinessLogic(unittest.TestCase):
    """Test suite for the business_logic.py module."""

    # Tests for type_of_patron
    def test_type_of_patron_negative_age(self):
        """Verify type_of_patron returns 'ERROR' for negative age."""
        self.assertEqual(type_of_patron(-1), "ERROR", "Negative age should return 'ERROR'.")

    def test_type_of_patron_minor(self):
        """Verify type_of_patron returns 'Minor' for ages under 18."""
        self.assertEqual(type_of_patron(17), "Minor", "Age 17 should return 'Minor'.")

    def test_type_of_patron_adult(self):
        """Verify type_of_patron returns 'Adult' for ages 18 to 89."""
        self.assertEqual(type_of_patron(30), "Adult", "Age 30 should return 'Adult'.")
        self.assertEqual(type_of_patron(89), "Adult", "Age 89 should return 'Adult'.")

    def test_type_of_patron_elderly(self):
        """Verify type_of_patron returns 'Elderly' for ages 90 and above."""
        self.assertEqual(type_of_patron(90), "Elderly", "Age 90 should return 'Elderly'.")
        self.assertEqual(type_of_patron(100), "Elderly", "Age 100 should return 'Elderly'.")

    # Tests for calculate_discount
    def test_calculate_discount_negative_age(self):
        """Verify calculate_discount returns 'ERROR' for negative age."""
        self.assertEqual(calculate_discount(-5), "ERROR", "Negative age should return 'ERROR'.")

    def test_calculate_discount_no_discount(self):
        """Verify calculate_discount returns 0 for patrons under 50."""
        self.assertEqual(calculate_discount(25), 0, "Age 25 should receive 0% discount.")
        self.assertEqual(calculate_discount(49), 0, "Age 49 should receive 0% discount.")

    def test_calculate_discount_10_percent(self):
        """Verify calculate_discount returns 10% for patrons aged 50 to 64."""
        self.assertEqual(calculate_discount(50), 10, "Age 50 should receive 10% discount.")
        self.assertEqual(calculate_discount(64), 10, "Age 64 should receive 10% discount.")

    def test_calculate_discount_15_percent(self):
        """Verify calculate_discount returns 15% for patrons aged 65 to 89."""
        self.assertEqual(calculate_discount(65), 15, "Age 65 should receive 15% discount.")
        self.assertEqual(calculate_discount(89), 15, "Age 89 should receive 15% discount.")

    def test_calculate_discount_100_percent(self):
        """Verify calculate_discount returns 100% for patrons aged 90 and above."""
        self.assertEqual(calculate_discount(90), 100, "Age 90 should receive 100% discount.")
        self.assertEqual(calculate_discount(120), 100, "Age 120 should receive 100% discount.")
        
    # Tests for can_borrow
    def test_can_borrow_book_allowed(self):
        """Verify can_borrow allows borrowing a Book when conditions are satisfied."""
        result = can_borrow(
            type_of_item="Book",
            patron_age=30,
            length_of_loan=30,
            outstanding_fees=0.0,
            gardening_tool_training=False,
            carpentry_tool_training=False
        )
        self.assertTrue(result, "Should allow borrowing Book with valid conditions.")

    def test_can_borrow_book_disallowed_due_to_fees(self):
        """Verify can_borrow disallows borrowing a Book if patron has outstanding fees."""
        result = can_borrow(
            type_of_item="Book",
            patron_age=30,
            length_of_loan=30,
            outstanding_fees=10.0,
            gardening_tool_training=False,
            carpentry_tool_training=False
        )
        self.assertFalse(result, "Should not allow borrowing Book when patron has fees.")

    def test_can_borrow_book_disallowed_due_to_loan_length(self):
        """Verify can_borrow disallows borrowing a Book if loan length exceeds limit."""
        result = can_borrow(
            type_of_item="Book",
            patron_age=30,
            length_of_loan=69,  # more than 56 days
            outstanding_fees=0.0,
            gardening_tool_training=False,
            carpentry_tool_training=False
        )
        self.assertFalse(result, "Should not allow borrowing Book when loan length exceeds limit.")

    def test_can_borrow_gardening_tool_disallowed_due_to_training(self):
        """Verify can_borrow disallows borrowing a Gardening tool if training is incomplete."""
        result = can_borrow(
            type_of_item="Gardening tool",
            patron_age=40,
            length_of_loan=20,
            outstanding_fees=0.0,
            gardening_tool_training=False,
            carpentry_tool_training=False
        )
        self.assertFalse(result, "Should not allow borrowing Gardening tool without training.")

    def test_can_borrow_gardening_tool_disallowed_due_to_loan_length(self):
        """Verify can_borrow disallows borrowing a Gardening tool if loan length exceeds limit."""
        result = can_borrow(
            type_of_item="Gardening tool",
            patron_age=40,
            length_of_loan=32,  # more than 28 days
            outstanding_fees=0.0,
            gardening_tool_training=True,
            carpentry_tool_training=False
        )
        self.assertFalse(result, "Should not allow borrowing Gardening tool when loan length exceeds limit.")

    def test_can_borrow_carpentry_tool_allowed(self):
        """Verify can_borrow allows borrowing a Carpentry tool when conditions are met."""
        result = can_borrow(
            type_of_item="Carpentry tool",
            patron_age=35,
            length_of_loan=10,
            outstanding_fees=0.0,
            gardening_tool_training=False,
            carpentry_tool_training=True
        )
        self.assertTrue(result, "Should allow borrowing Carpentry tool with valid conditions.")

    def test_can_borrow_carpentry_tool_disallowed_due_to_fees(self):
        """Verify can_borrow disallows borrowing a Carpentry tool if patron has outstanding fees."""
        result = can_borrow(
            type_of_item="Carpentry tool",
            patron_age=35,
            length_of_loan=10,
            outstanding_fees=15.0,
            gardening_tool_training=False,
            carpentry_tool_training=True
        )
        self.assertFalse(result, "Should not allow borrowing Carpentry tool when patron has fees.")

    def test_can_borrow_carpentry_tool_without_training(self):
        """Verify can_borrow disallows borrowing a Carpentry tool if training is incomplete."""
        result = can_borrow(
            type_of_item="Carpentry tool",
            patron_age=35,
            length_of_loan=10,
            outstanding_fees=0.0,
            gardening_tool_training=False,
            carpentry_tool_training=False
        )
        self.assertFalse(result, "Should not allow borrowing Carpentry tool without training.")

    def test_can_borrow_carpentry_tool_disallowed_due_to_patron_type(self):
        """Verify can_borrow disallows borrowing a Carpentry tool if patron is not an adult or is elderly."""
        # Patron age <=18
        result_minor = can_borrow(
            type_of_item="Carpentry tool",
            patron_age=18,
            length_of_loan=10,
            outstanding_fees=0.0,
            gardening_tool_training=False,
            carpentry_tool_training=True
        )
        self.assertFalse(result_minor, "Should not allow borrowing Carpentry tool if patron is a minor.")

        # Patron age >=90
        result_elderly = can_borrow(
            type_of_item="Carpentry tool",
            patron_age=90,
            length_of_loan=10,
            outstanding_fees=0.0,
            gardening_tool_training=False,
            carpentry_tool_training=True
        )
        self.assertFalse(result_elderly, "Should not allow borrowing Carpentry tool if patron is elderly.")

    def test_can_borrow_carpentry_tool_with_zero_fees_and_training(self):
        """Verify can_borrow allows borrowing a Carpentry tool with zero fees and completed training."""
        result = can_borrow(
            type_of_item="Carpentry tool",
            patron_age=65,
            length_of_loan=14,
            outstanding_fees=0.0,
            gardening_tool_training=False,
            carpentry_tool_training=True
        )
        self.assertTrue(result, "Should allow borrowing Carpentry tool with zero fees and completed training.")

    # Tests for can_use_makerspace
    def test_can_use_makerspace_allowed(self):
        """Test can_use_makerspace when all conditions are met."""
        result = can_use_makerspace(
            patron_age=30,
            outstanding_fees=0.0,
            makerspace_training=True
        )
        self.assertTrue(result, "Should allow makerspace access when all conditions are met.")

    def test_can_use_makerspace_disallowed_due_to_fees(self):
        """Test can_use_makerspace when patron has outstanding fees."""
        result = can_use_makerspace(
            patron_age=30,
            outstanding_fees=10.0,
            makerspace_training=True
        )
        self.assertFalse(result, "Should not allow makerspace access when patron has fees.")

    def test_can_use_makerspace_disallowed_due_to_training(self):
        """Test can_use_makerspace when patron hasn't completed training."""
        result = can_use_makerspace(
            patron_age=30,
            outstanding_fees=0.0,
            makerspace_training=False
        )
        self.assertFalse(result, "Should not allow makerspace access without training.")

    def test_can_use_makerspace_disallowed_due_to_patron_type(self):
        """Test can_use_makerspace when patron is not an adult."""
        # Patron is Minor
        result_minor = can_use_makerspace(
            patron_age=17,
            outstanding_fees=0.0,
            makerspace_training=True
        )
        self.assertFalse(result_minor, "Should not allow makerspace access if patron is minor.")

        # Patron is Elderly
        result_elderly = can_use_makerspace(
            patron_age=90,
            outstanding_fees=0.0,
            makerspace_training=True
        )
        self.assertFalse(result_elderly, "Should not allow makerspace access if patron is elderly.")

    def test_can_use_makerspace_error_patron_type(self):
        """Test can_use_makerspace when patron_type is ERROR."""
        # Mock type_of_patron to return "ERROR"
        with mock.patch('src.business_logic.type_of_patron', return_value="ERROR"):
            result = can_use_makerspace(
                patron_age=-5,
                outstanding_fees=0.0,
                makerspace_training=True
            )
            self.assertFalse(result, "Should not allow makerspace access when patron_type is 'ERROR'.")

    # Tests for process_loan
    @mock.patch('src.business_logic.can_borrow', return_value=True)
    def test_process_loan_successful(self, mock_can_borrow):
        """Test process_loan when borrowing conditions are met."""
        # Arrange
        patron = Patron()
        patron.set_new_patron_data(id=1, name="John Doe", age=30)
        item = BorrowableItem()
        # Manually set attributes
        item._id = 1
        item._name = "Book1"
        item._type = "Book"
        item._year = 2020
        item._number_owned = 5
        item._on_loan = 0
        length_of_loan = 10

        # Act
        result = process_loan(patron, item, length_of_loan)

        # Assert
        self.assertTrue(result, "Loan should be successful when can_borrow returns True.")
        self.assertEqual(len(patron._loans), 1, "Patron should have one loan after successful loan.")
        self.assertEqual(item._on_loan, 1, "Item's _on_loan should be incremented by 1.")
        mock_can_borrow.assert_called_once_with(
            item._type,
            patron._age,
            length_of_loan,
            patron._outstanding_fees,
            patron._gardening_tool_training,
            patron._carpentry_tool_training
        )

    @mock.patch('src.business_logic.can_borrow', return_value=False)
    def test_process_loan_disallowed(self, mock_can_borrow):
        """Test process_loan when borrowing conditions are not met."""
        # Arrange
        patron = Patron()
        patron.set_new_patron_data(id=2, name="Jane Smith", age=30)
        patron._outstanding_fees = 10.0  # Set fees to make can_borrow return False
        item = BorrowableItem()
        item._id = 2
        item._name = "Book2"
        item._type = "Book"
        item._year = 2021
        item._number_owned = 3
        item._on_loan = 1
        length_of_loan = 10

        # Act
        result = process_loan(patron, item, length_of_loan)

        # Assert
        self.assertFalse(result, "Loan should be unsuccessful when can_borrow returns False.")
        self.assertEqual(len(patron._loans), 0, "Patron should have no loans after unsuccessful loan.")
        self.assertEqual(item._on_loan, 1, "Item's _on_loan should remain unchanged.")
        mock_can_borrow.assert_called_once_with(
            item._type,
            patron._age,
            length_of_loan,
            patron._outstanding_fees,
            patron._gardening_tool_training,
            patron._carpentry_tool_training
        )

    # Tests for process_return 
    def test_process_return_successful(self):
        """Test process_return when the patron has the loan."""
        # Arrange
        patron = Patron()
        patron.set_new_patron_data(id=8, name="Fiona Hill", age=30)
        item = BorrowableItem()
        item._id = 8
        item._name = "Book8"
        item._type = "Book"
        item._year = 2014
        item._number_owned = 2
        item._on_loan = 1
        loan = Loan(item, date.today() + timedelta(days=10))
        patron._loans.append(loan)

        # Act
        process_return(patron, item_id=8)

        # Assert
        self.assertEqual(len(patron._loans), 0, "Patron should have no loans after returning.")
        self.assertEqual(item._on_loan, 1, "Item's _on_loan should remain unchanged due to bug.")

    def test_process_return_no_loan_found(self):
        """Test process_return when the patron does not have the loan."""
        # Arrange
        patron = Patron()
        patron.set_new_patron_data(id=9, name="George Moore", age=30)
        item = BorrowableItem()
        item._id = 9
        item._name = "Book9"
        item._type = "Book"
        item._year = 2013
        item._number_owned = 1
        item._on_loan = 1

        # Act & Assert
        with self.assertRaises(AttributeError):
            process_return(patron, item_id=10)  # Item ID 10 not loaned

    def test_process_return_invalid_item_id(self):
        """Test process_return with an invalid item ID."""
        # Arrange
        patron = Patron()
        patron.set_new_patron_data(id=10, name="Hannah Nelson", age=30)
        # No loans added

        # Act & Assert
        with self.assertRaises(AttributeError):
            process_return(patron, item_id=999)  # Non-existent item ID

    def test_process_return_modifies_item_and_patron_loans(self):
        """Test that process_return correctly modifies item and patron loans."""
        # Arrange
        patron = Patron()
        patron.set_new_patron_data(id=12, name="Jessica Quinn", age=30)
        item = BorrowableItem()
        item._id = 13
        item._name = "Book13"
        item._type = "Book"
        item._year = 2010
        item._number_owned = 1
        item._on_loan = 2
        loan = Loan(item, date.today() + timedelta(days=10))
        patron._loans.append(loan)

        # Act
        process_return(patron, item_id=13)

        # Assert
        self.assertEqual(len(patron._loans), 0, "Patron should have no loans after returning.")
        self.assertEqual(item._on_loan, 2, "Item's _on_loan should remain unchanged due to bug.")

    def test_process_return_with_no_loans(self):
        """Test process_return when patron has no loans."""
        # Arrange
        patron = Patron()
        patron.set_new_patron_data(id=13, name="Kevin Roberts", age=30)
        item = BorrowableItem()
        item._id = 14
        item._name = "Book14"
        item._type = "Book"
        item._year = 2009
        item._number_owned = 1
        item._on_loan = 0

        # Act & Assert
        with self.assertRaises(AttributeError):
            process_return(patron, item_id=14)  # No loans exist