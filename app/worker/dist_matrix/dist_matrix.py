from typing import List, Tuple, Dict, Union
import json
import os
import logging
logging.basicConfig(filename='/app/log/dist_matrix.log', level=logging.DEBUG)
import requests

from django.conf import settings

class DistMatrix:
    """
    Based on given input (dict of addr_id and their coordinates)
    Generate distance matrix
    Also saves data to local disk/cloud mongodb
    """

    trip_id: int
    dist_matrix: List[List[int]]
    addr_map: Dict[str, Dict[str, List[float]]]
    logger = logging.getLogger(__name__)

    def __init__(self, addr_map: Dict):
        self.addr_map = addr_map
        self.trip_id = addr_map["tripId"]
        self.dist_matrix = []
    
    @staticmethod
    def get_dist_matrix_path(trip_id: int) -> str:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        return settings.DIST_MATRIX_PATH + "/" + str(trip_id) + ".json"
    
    @staticmethod
    def get_route_path(trip_id: int) -> str:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        return settings.ROUTE_PATH + "/" + str(trip_id) + ".json"

    @staticmethod
    def get_google_maps_distance(origin_lat: float, origin_lng: float, dest_lat: float, dest_lng: float) -> int:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        url: str = settings.GOOGLE_MAPS["GOOGLE_MAPS_API_URL"]
        url = url.replace("<origin-lat>", str(origin_lat))\
                .replace("<origin-lng>", str(origin_lng))\
                .replace("<dest-lat>", str(dest_lat))\
                .replace("<dest-lng>", str(dest_lng))
        response: requests.Response = requests.get(url)

        # This is duration in unit of seconds
        duration_sec: int = response.json()["rows"][0]["elements"][0]["duration"]["value"]
        return duration_sec
    
    def save_dist_matrix(self) -> None:
        with open(self.get_dist_matrix_path(self.trip_id), "w") as f:
            json.dump(self.dist_matrix, f)
        self.logger.info(f"{self.get_dist_matrix_path(self.trip_id)} saved")
    
    def get_dist_matrix(self) -> List[List[int]]:
        with open(self.get_dist_matrix_path(self.trip_id), "r") as f:
            return json.load(f)

    def generate_dist_matrix_helper(self) -> None:
        # Python does not support local variables in for-loop
        # I've got to move typing outside the for-loop
        # So annoying
        row: int
        col: int
        origin_lat: float
        origin_lng: float
        dest_lat:   float
        dest_lng:   float

        curr_len:   int = len(self.dist_matrix)
        target_len: int = len(self.addr_map["addrs"])

        # Reset if after reloading
        if target_len < curr_len: curr_len = 0

        # Expand existing rows (expanding to the right)
        for row in range(curr_len):
            for col in range(curr_len, target_len):
                origin_lat  = self.addr_map["addrs"][str(row)][0]
                origin_lng  = self.addr_map["addrs"][str(row)][1]
                dest_lat    = self.addr_map["addrs"][str(col)][0]
                dest_lng    = self.addr_map["addrs"][str(col)][1]
                self.dist_matrix[row].append(self.get_google_maps_distance(origin_lat, origin_lng, dest_lat, dest_lng))

        # New rows (expanding down)
        for row in range(curr_len, target_len):
            self.dist_matrix.append([])
            for col in range(target_len):
                if row == col:
                    self.dist_matrix[row].append(0)
                    continue

                origin_lat = self.addr_map["addrs"][str(row)][0]
                origin_lng = self.addr_map["addrs"][str(row)][1]
                dest_lat   = self.addr_map["addrs"][str(col)][0]
                dest_lng   = self.addr_map["addrs"][str(col)][1]
                self.dist_matrix[row].append(self.get_google_maps_distance(origin_lat, origin_lng, dest_lat, dest_lng))
        
        self.logger.info(f"{self.get_dist_matrix_path(self.trip_id)} generated, saving")
        self.save_dist_matrix()

    def generate_dist_matrix(self) -> None:
        """
        Generate dist matrix based on given addr_map
        If dist_matrix already exists, will only generate those new rows/cols
        To avoid unnecessary calls to Google Maps API
        """
        if self.dist_matrix_exists():
            self.logger.info(f"{self.get_dist_matrix_path(self.trip_id)} exist, checking if has same number of addrs")
            with open(self.get_dist_matrix_path(self.trip_id), "r") as f:
                self.dist_matrix: List[List[int]] = json.load(f)

            if len(self.dist_matrix) == len(self.addr_map["addrs"]):
                self.logger.info(f"{self.get_dist_matrix_path(self.trip_id)} has same number of addrs, returning directly (no generation needed)")
                return
            else:
                self.logger.info(f"{self.get_dist_matrix_path(self.trip_id)} does not have same number of addrs, generating new (by increment)")
        
        else:
            self.logger.info(f"{self.get_dist_matrix_path(self.trip_id)} not exist, generating new (all of them)")
        
        self.generate_dist_matrix_helper()

    def dist_matrix_exists(self) -> bool:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        if not os.path.exists(settings.DIST_MATRIX_PATH):
            self.logger.info(f'{settings.DIST_MATRIX_PATH} does not exist, creating')
            os.makedirs(settings.DIST_MATRIX_PATH)
            return False
        if not os.path.exists(self.get_dist_matrix_path(self.trip_id)):
            return False
        return True
    
    def route_exits(self) -> bool:
        if not os.path.exists(settings.ROUTE_PATH):
            self.logger.info(f'{settings.ROUTE_PATH} does not exist, creating')
            os.makedirs(settings.ROUTE_PATH)
            return False
        if not os.path.exists(self.get_route_path(self.trip_id)):
            return False
        return True