from typing import List, Dict
import unittest
import json
import sys
sys.path.append(".")
from dist_matrix import DistMatrix

class DistMatrixTest(unittest.TestCase):

    @unittest.skip("Skipping Google Maps API. Already passed test")
    def test_get_google_maps_distance(self):
        origin_lat: float =  38.652674
        origin_lng: float = -90.295012
        dest_lat:   float =  38.647387
        dest_lng:   float = -90.309698

        # Test this static method
        duration_sec: int = DistMatrix.get_google_maps_distance(origin_lat, origin_lng, dest_lat, dest_lng)
        print(f"Duration in seconds: {duration_sec}")
    
    @unittest.skip("Passed")
    def test_get_dist_matrix_path(self):
        path: str = DistMatrix.get_dist_matrix_path(1024)
        print(path)

    @unittest.skip("Passed")
    def test_get_route_path(self):
        path: str = DistMatrix.get_route_path(1024)
        print(path)

    def test_dist_matrix(self):
        file_path: str = "/app/data/dist_matrix/sample_addr_map.json"
        with open(file_path, "r") as f:
            print(f" ===== Reading now: {file_path}  =====")
            addr_map: Dict[str, List[float]] = json.load(f)
            
            dist_matrix: DistMatrix = DistMatrix(addr_map)
            dist_matrix.generate_dist_matrix()

if __name__ == "__main__":
    unittest.main()