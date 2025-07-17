import unittest
from unittest.mock import patch, MagicMock
from CTA_Ingestor import __init__ as main

class TestIngestor(unittest.TestCase):

    @patch('CTA_Ingestor.__init__.requests.get')
    def test_get_bus_positions(self, mock_get):
        # Mock API response
        mock_get.return_value.json.return_value = {
            "bustime-response": {"vehicle": [{"id": "bus1"}]}
        }

        buses = main.get_bus_positions()
        self.assertEqual(len(buses), 1)

    # Add more tests for error handling, event sending, etc.