from typing import List, Dict
import unittest
import json
import sys
sys.path.append(".")
from dist_matrix.dist_matrix import DistMatrix
from dist_matrix.formatter import Formatter
from tsp.held_karp import HeldKarp
import logging
logger = logging.getLogger(__name__)
import requests

def optimise_route(trip: Dict):
    formatter: Formatter = Formatter(trip)
    addr_map: Dict = formatter.get_addr_map()

    logger.info("Generating distance matrix...")
    dist_matrix: DistMatrix = DistMatrix(addr_map)
    dist_matrix.generate_dist_matrix()
    logger.info("Done generating distance matrix...")

    held_karp = HeldKarp(dist_matrix.get_dist_matrix())
    min_cost: int
    path: List[int]
    min_cost, path = held_karp.tsp_shortest_path()
    trip_route: Dict = formatter.get_trip_route(path)

    res: Dict = {
        "min_cost": min_cost,
        "path": path
    }

    print(res)

class TasksTest(unittest.TestCase):

    @unittest.skip("Passed")
    def test_optimise_route(self):
        file_path: str = "/app/data/dist_matrix/sample_addr_map.json"
        with open(file_path, "r") as f:
            print(f" ===== Reading now: {file_path}  =====")
            addr_map: Dict[str, List[float]] = json.load(f)
        optimise_route(addr_map)

    @unittest.skip("skipped")
    def test_optimise_route_2(self):
        trip: Dict = {
            "id":1,
            "passcode":"TAX108",
            "startTime":1604878200000,
            "finishTime":None,
            "isRouteUpToDate":False,
            "route":[
                {
                "id":3,
                "riderId":2,
                "addr":"600 Warren Rd, Ithaca, NY",
                "lat":42.478183,
                "lng":-76.467121,
                "hasArrived":False,
                "boardingTime":None,
                "arrivalTime":None,
                "seqId":0
                },
                {
                "id":5,
                "riderId":4,
                "addr":"210 Summerhill Dr, Ithaca, Ny",
                "lat":42.43720545,
                "lng":-76.4598289420636,
                "hasArrived":False,
                "boardingTime":None,
                "arrivalTime":None,
                "seqId":0
                }
            ]
        }
        formatter: Formatter = Formatter(trip)
        addr_map: Dict = formatter.get_addr_map()

        logger.info("Generating distance matrix...")
        dist_matrix: DistMatrix = DistMatrix(addr_map)
        dist_matrix.generate_dist_matrix()
        logger.info("Done generating distance matrix...")

        held_karp = HeldKarp(dist_matrix.get_dist_matrix())
        min_cost: int
        path: List[int]
        min_cost, path = held_karp.tsp_shortest_path()
        trip_route: Dict = formatter.get_trip_route(path)

        print(trip_route)
    
    @unittest.skip("skipped")
    def test_optimise_route_3(self):
        trip: Dict = {
            "id":1,
            "passcode":"HEY668",
            "startTime":1604878200000,
            "finishTime":None,
            "isRouteUpToDate":False,
            "route":[
                {
                "id":3,
                "riderId":2,
                "addr":"600 Warren Rd, Ithaca, NY",
                "lat":42.478183,
                "lng":-76.467121,
                "hasArrived":False,
                "boardingTime":None,
                "arrivalTime":None,
                "seqId":0
                }
            ]
        }
        formatter: Formatter = Formatter(trip)
        addr_map: Dict = formatter.get_addr_map()

        logger.info("Generating distance matrix...")
        dist_matrix: DistMatrix = DistMatrix(addr_map)
        dist_matrix.generate_dist_matrix()
        logger.info("Done generating distance matrix...")

        held_karp = HeldKarp(dist_matrix.get_dist_matrix())
        min_cost: int
        path: List[int]
        min_cost, path = held_karp.tsp_shortest_path()
        trip_route: Dict = formatter.get_trip_route(path)

        print(trip_route)

        url: str = "https://host.docker.internal:8080/jpa/system/trip/<id>/update-route".replace("<id>", str(trip_route["tripId"]))
        r: requests.Response = requests.post(url, json=trip_route, verify=False)
    
    def test_optimise_route_4(self):
        trip: Dict = {
            "id":20001,
            "passcode":"TAR256",
            "startTime":1604878200000,
            "finishTime":None,
            "isRouteUpToDate":False,
            "route":[
                {
                "id":30001,
                "riderId":10003,
                "addr":"210 Summerhill Dr, Ithaca, NY",
                "lat":42.436688,
                "lng":-76.459556,
                "hasArrived":False,
                "boardingTime":None,
                "arrivalTime":None,
                "seqId":0
                }
            ]
        }
        formatter: Formatter = Formatter(trip)
        addr_map: Dict = formatter.get_addr_map()

        logger.info("Generating distance matrix...")
        dist_matrix: DistMatrix = DistMatrix(addr_map)
        dist_matrix.generate_dist_matrix()
        logger.info("Done generating distance matrix...")

        held_karp = HeldKarp(dist_matrix.get_dist_matrix())
        min_cost: int
        path: List[int]
        min_cost, path = held_karp.tsp_shortest_path()
        trip_route: Dict = formatter.get_trip_route(path)

        print(trip_route)

        url: str = "https://host.docker.internal:8080/jpa/system/trip/<id>/update-route".replace("<id>", str(trip_route["tripId"]))
        headers: Dict = {"Content-Type": "application/json"}
        r: requests.Response = requests.post(url, data=json.dumps(trip_route), headers=headers, verify=False)


if __name__ == "__main__":
    unittest.main()