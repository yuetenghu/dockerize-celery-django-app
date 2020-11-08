from typing import List, Dict
import unittest
import json
import sys
sys.path.append(".")
from formatter import Formatter

class FormatterTest(unittest.TestCase):

    def test_formatter(self):
        file_path: str = "/app/data/dist_matrix/sample_trip.json"
        with open(file_path, "r") as f:
            trip: Dict = json.load(f)
        
        formatter: Formatter = Formatter(trip)
        addr_map: Dict = formatter.get_addr_map()
        trip_route: Dict = formatter.get_trip_route([0, 3, 1, 2, 0])
        print(addr_map)
        print(trip_route)

if __name__ == "__main__":
    unittest.main()