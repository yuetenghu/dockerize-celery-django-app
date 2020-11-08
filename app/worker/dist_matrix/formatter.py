from typing import List, Tuple, Dict
import logging
logging.basicConfig(filename='/app/log/formatter.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Formatter:
    """
    Translate between trip and addr_map
    """

    trip: Dict
    addr_map: Dict
    city_id_to_addr_id: List[int]
    trip_route: Dict
    
    START_POINT: List = [42.445368, -76.483413, "Sage Hall Car Park"]

    def __init__(self, trip: Dict):
        self.trip = trip
        self.addr_map = {
            "tripId": trip["id"],
            "addrs": {
                "0": self.START_POINT
            }
        }
        self.city_id_to_addr_id = [0]
        self.trip_route = {"tripId": trip["id"]}
    
    def get_addr_map(self) -> Dict:
        i: int
        for i in range(len(self.trip["route"])):
            addr: Dict = self.trip["route"][i]
            self.addr_map["addrs"][str(i + 1)] = [addr["lat"], addr["lng"], addr["addr"]]
            self.city_id_to_addr_id.append(addr["id"])
        return self.addr_map
    
    def get_trip_route(self, shortest_path: List[int]) -> Dict:
        logger.info(f'get_trip_route(): shortest_path = {shortest_path}')
        route: List[int] = []
        city_id: int
        for city_id in shortest_path:
            if city_id == 0: continue
            route.append(self.city_id_to_addr_id[city_id])
        self.trip_route["seqIds"] = route
        return self.trip_route