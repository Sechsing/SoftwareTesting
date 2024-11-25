import unittest
from src.search import find_patron_by_name, find_patron_by_age, find_patron_by_name_and_age, find_item_by_id
from src.patron import Patron
from src.borrowable_item import BorrowableItem

class TestSearchFunctions(unittest.TestCase):

    def setUp(self):
        """Set up mock patrons and borrowable items for tests."""
        # Create mock patrons
        self.patron1 = Patron()
        self.patron1.set_new_patron_data(1, "Alice", 30)
        self.patron2 = Patron()
        self.patron2.set_new_patron_data(2, "Bob", 25)
        self.patron3 = Patron()
        self.patron3.set_new_patron_data(3, "Charlie", 30)
        
        self.patrons = [self.patron1, self.patron2, self.patron3]

        # Create mock borrowable items
        self.item1 = BorrowableItem()
        self.item1.load_data({
            "item_id": 1,
            "item_name": "The Great Gatsby",
            "item_type": "Book",
            "year": 1925,
            "number_owned": 5,
            "on_loan": 1
        })
        self.item2 = BorrowableItem()
        self.item2.load_data({
            "item_id": 2,
            "item_name": "Gardening Basics",
            "item_type": "Gardening tool",
            "year": 2020,
            "number_owned": 10,
            "on_loan": 0
        })
        self.items = [self.item1, self.item2]

    def test_find_patron_by_name(self):
        """Test finding patrons by name."""
        result = find_patron_by_name("Alice", self.patrons)
        self.assertEqual(len(result), 1, "Should find one patron named Alice.")
        self.assertEqual(result[0]._id, 1, "Found patron ID should be 1.")
        
        result = find_patron_by_name("David", self.patrons)
        self.assertEqual(len(result), 0, "Should find no patrons named David.")

    def test_find_patron_by_age(self):
        """Test finding patrons by age."""
        result = find_patron_by_age(30, self.patrons)
        self.assertEqual(len(result), 2, "Should find two patrons aged 30.")
        self.assertIn(self.patron1, result, "Alice should be in the result.")
        self.assertIn(self.patron3, result, "Charlie should be in the result.")

        result = find_patron_by_age(25, self.patrons)
        self.assertEqual(len(result), 1, "Should find one patron aged 25.")
        self.assertEqual(result[0]._id, 2, "Found patron ID should be 2.")

        result = find_patron_by_age(40, self.patrons)
        self.assertEqual(len(result), 0, "Should find no patrons aged 40.")

    def test_find_patron_by_name_and_age(self):
        """Test finding a patron by name and age."""
        result = find_patron_by_name_and_age("Alice", 30, self.patrons)
        self.assertIsNotNone(result, "Should find patron Alice aged 30.")
        self.assertEqual(result._id, 1, "Found patron ID should be 1.")
        
        result = find_patron_by_name_and_age("Bob", 30, self.patrons)
        self.assertIsNone(result, "Should not find patron Bob aged 30.")
        
        result = find_patron_by_name_and_age("Charlie", 25, self.patrons)
        self.assertIsNone(result, "Should not find patron Charlie aged 25.")

    def test_find_item_by_id(self):
        """Test finding items by ID."""
        result = find_item_by_id(1, self.items)
        self.assertIsNotNone(result, "Should find item with ID 1.")
        self.assertEqual(result._id, 1, "Found item ID should be 1.")

        result = find_item_by_id(2, self.items)
        self.assertIsNotNone(result, "Should find item with ID 2.")
        self.assertEqual(result._id, 2, "Found item ID should be 2.")

        result = find_item_by_id(999, self.items)
        self.assertIsNone(result, "Should not find an item with a non-existent ID.")
