import unittest
from unittest.mock import patch
from src.user_input import (
    is_int,
    is_float,
    read_string,
    read_integer,
    read_float,
    read_integer_range,
    read_float_range,
    read_bool
)

class TestUserInput(unittest.TestCase):

    # Tests for is_int
    def test_is_int_valid(self):
        self.assertTrue(is_int("10"))
        self.assertTrue(is_int("-5"))
        self.assertTrue(is_int("0"))

    def test_is_int_invalid(self):
        self.assertFalse(is_int("10.5"))
        self.assertFalse(is_int("abc"))
        self.assertFalse(is_int(""))

    # Tests for is_float
    def test_is_float_valid(self):
        self.assertTrue(is_float("10.5"))
        self.assertTrue(is_float("-5.5"))
        self.assertTrue(is_float("0.0"))
        self.assertTrue(is_float("10"))

    def test_is_float_invalid(self):
        self.assertFalse(is_float("abc"))
        self.assertFalse(is_float(""))

    # Tests for read_string
    @patch('builtins.input', side_effect=["test_string"])
    def test_read_string(self, mock_input):
        result = read_string("Enter a string: ")
        self.assertEqual(result, "test_string")

    # Tests for read_integer
    @patch('builtins.input', side_effect=["abc", "10"])
    def test_read_integer_valid(self, mock_input):
        result = read_integer("Enter an integer: ")
        self.assertEqual(result, 10)

    @patch('builtins.input', side_effect=["10.5", "5"])
    def test_read_integer_invalid(self, mock_input):
        result = read_integer("Enter an integer: ")
        self.assertEqual(result, 5)

    # Tests for read_float
    @patch('builtins.input', side_effect=["abc", "10.5"])
    def test_read_float_valid(self, mock_input):
        result = read_float("Enter a float: ")
        self.assertEqual(result, 10.5)

    @patch('builtins.input', side_effect=["abc", "5.5"])  # Valid float after invalid
    def test_read_float_invalid(self, mock_input):
        result = read_float("Enter a float: ")
        self.assertEqual(result, 5.5)

    # Tests for read_integer_range
    @patch('builtins.input', side_effect=["12", "-5", "10"])
    def test_read_integer_range_valid(self, mock_input):
        result = read_integer_range("Enter an integer between 1 and 10: ", 1, 10)
        self.assertEqual(result, 10)

    @patch('builtins.input', side_effect=["0", "11", "5"])  # Testing invalid before valid
    def test_read_integer_range_invalid(self, mock_input):
        result = read_integer_range("Enter an integer between 1 and 10: ", 1, 10)
        self.assertEqual(result, 5)

    # Tests for read_float_range
    @patch('builtins.input', side_effect=["15.0", "-5.5", "10.0"])  # Adjusted for testing valid
    def test_read_float_range_valid(self, mock_input):
        result = read_float_range("Enter a float between 1.0 and 10.0: ", 1.0, 10.0)
        self.assertEqual(result, 10.0)

    @patch('builtins.input', side_effect=["0", "11.0", "5.5"])  # Invalid before valid
    def test_read_float_range_invalid(self, mock_input):
        result = read_float_range("Enter a float between 1.0 and 10.0: ", 1.0, 10.0)
        self.assertEqual(result, 5.5)

    # Tests for read_bool
    @patch('builtins.input', side_effect=["abc", "y"])
    def test_read_bool_valid(self, mock_input):
        result = read_bool("Enter 'y' or 'n': ")
        self.assertEqual(result, 'y')

    @patch('builtins.input', side_effect=["n", "N"])
    def test_read_bool_case_insensitive(self, mock_input):
        result = read_bool("Enter 'y' or 'n': ")
        self.assertEqual(result, 'n')

    @patch('builtins.input', side_effect=["abc", "y"])
    def test_read_bool_invalid(self, mock_input):
        result = read_bool("Enter 'y' or 'n': ")
        self.assertEqual(result, 'y')

if __name__ == '__main__':
    unittest.main()
