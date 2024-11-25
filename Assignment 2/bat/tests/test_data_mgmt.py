import unittest
import json
import sys

from unittest.mock import patch
from src.data_mgmt import DataManager
from src.patron import Patron
from src.borrowable_item import BorrowableItem
import src.config as config

class TestDataManager(unittest.TestCase):

    @patch('src.data_mgmt.DataManager.load_patrons')
    @patch('src.data_mgmt.DataManager.load_catalogue')
    def setUp(self, mock_load_catalogue, mock_load_patrons):
        # Create a DataManager instance
        self.dm = DataManager()

        # Manually set up initial patron data
        self.dm._patron_data = [
            Patron(),
            Patron()
        ]
        self.dm._patron_data[0].set_new_patron_data(1, "Alice", 30)
        self.dm._patron_data[1].set_new_patron_data(2, "Bob", 25)

        # Manually set up initial catalogue data
        self.dm._catalogue_data = [
            BorrowableItem(),
            BorrowableItem()
        ]
        self.dm._catalogue_data[0]._id = 1
        self.dm._catalogue_data[0]._name = "Hammer"
        self.dm._catalogue_data[0]._type = "Tool"
        self.dm._catalogue_data[0]._year = 2020
        self.dm._catalogue_data[0]._number_owned = 10
        self.dm._catalogue_data[0]._on_loan = 2

        self.dm._catalogue_data[1]._id = 2
        self.dm._catalogue_data[1]._name = "Saw"
        self.dm._catalogue_data[1]._type = "Tool"
        self.dm._catalogue_data[1]._year = 2019
        self.dm._catalogue_data[1]._number_owned = 5
        self.dm._catalogue_data[1]._on_loan = 1

    def test_register_patron(self):
        # Register a new patron
        self.dm.register_patron("Charlie", 20)

        # Check that the new patron has been added
        self.assertEqual(len(self.dm._patron_data), 3)

        # Check the details of the new patron
        new_patron = self.dm._patron_data[-1]
        self.assertEqual(new_patron._id, 3)
        self.assertEqual(new_patron._name, "Charlie")
        self.assertEqual(new_patron._age, 20)
        self.assertEqual(new_patron._outstanding_fees, 0.0)
        self.assertFalse(new_patron._gardening_tool_training)
        self.assertFalse(new_patron._carpentry_tool_training)
        self.assertFalse(new_patron._makerspace_training)

    @patch('json.load')
    def test_load_patrons_success(self, mock_json_load):
        """Test successful loading of patrons from a file."""
        # Mock the loaded JSON data matching the initial setup
        mock_json_load.return_value = [
            {
                "patron_id": 1, 
                "name": "Alice", 
                "age": 30, 
                "outstanding_fees": 0.0,
                "loans": [],
                "gardening_tool_training": False,  # Add missing training fields
                "carpentry_tool_training": False,
                "makerspace_training": False
            },
            {
                "patron_id": 2, 
                "name": "Bob", 
                "age": 25, 
                "outstanding_fees": 0.0,
                "loans": [],
                "gardening_tool_training": False,  # Add missing training fields
                "carpentry_tool_training": False,
                "makerspace_training": False
            }
        ]

        # Load patrons
        with patch('builtins.open'):
            self.dm.load_patrons()

        # Verify that patron data is loaded correctly
        self.assertEqual(len(self.dm._patron_data), 2)
        self.assertEqual(self.dm._patron_data[0]._name, "Alice")
        self.assertEqual(self.dm._patron_data[1]._name, "Bob")

    @patch('builtins.open')
    @patch('sys.exit')
    def test_load_patrons_failure(self, mock_exit, mock_open):
        mock_open.side_effect = IOError
        self.dm.load_patrons()
        mock_exit.assert_called_once()

    @patch('json.load')
    def test_load_catalogue_success(self, mock_json_load):
        """Test successful loading of catalogue data."""
        mock_json_load.return_value = [
            {"item_id": 1, "item_name": "Hammer", "item_type": "Tool", "year": 2020, "number_owned": 10, "on_loan": 2},
            {"item_id": 2, "item_name": "Saw", "item_type": "Tool", "year": 2019, "number_owned": 5, "on_loan": 1}
        ]
        with patch('builtins.open'):
            self.dm.load_catalogue()

        # Verify catalogue data is loaded correctly
        self.assertEqual(len(self.dm._catalogue_data), 2)
        self.assertEqual(self.dm._catalogue_data[0]._name, "Hammer")
        self.assertEqual(self.dm._catalogue_data[1]._name, "Saw")

    @patch('builtins.open')
    @patch('sys.exit')
    def test_load_catalogue_failure(self, mock_exit, mock_open):
        mock_open.side_effect = IOError
        self.dm.load_catalogue()
        mock_exit.assert_called_once()

    @patch('builtins.open')
    @patch('json.dumps')
    @patch('sys.exit')
    def test_save_patrons(self, mock_exit, mock_json_dumps, mock_open):
        mock_open.return_value.__enter__.return_value.write = lambda x: None  # Mock the file write
        self.dm.save_patrons()
        mock_open.assert_called_once_with(config.PATRON_DATA, 'w')
        mock_json_dumps.assert_called()
        mock_exit.assert_not_called()

    @patch('builtins.open')
    @patch('json.dumps')
    @patch('sys.exit')
    def test_save_catalogue(self, mock_exit, mock_json_dumps, mock_open):
        mock_open.return_value.__enter__.return_value.write = lambda x: None  # Mock the file write
        self.dm.save_catalogue()
        mock_open.assert_called_once_with(config.CATALOGUE_DATA, 'w')
        mock_json_dumps.assert_called()
        mock_exit.assert_not_called()

if __name__ == '__main__':
    unittest.main()
