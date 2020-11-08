from typing import Dict, List
import os
import logging
logging.basicConfig(filename='/app/log/tasks.log', level=logging.DEBUG)
import requests
import json

# from celery.utils.log import get_task_logger
from .worker import app
from django.conf import settings

from .dist_matrix.dist_matrix import DistMatrix
from .dist_matrix.formatter import Formatter
from .tsp.held_karp import HeldKarp

logger = logging.getLogger(__name__)
# logger = get_task_logger(__name__)


@app.task(bind=True, name='fetch_data_from_quandl')
def fetch_data_from_quandl(self, database_code, dataset_code):
    url = f'https://www.quandl.com/api/v3/datasets/{database_code}/{dataset_code}/data.json'
    response = requests.get(url)
    logger.info(f'GET {url} returned status_code {response.status_code}')
    if response.ok:
        if not os.path.exists(settings.DATA_PATH):
            logger.info(f'{settings.DATA_PATH} does not exist, create')
            os.makedirs(settings.DATA_PATH)
        slug = f'{database_code}-{dataset_code}'
        logger.info(f'Write data to {slug}')
        with open(os.path.join(settings.DATA_PATH, slug), 'w') as f:
            f.write(response.text)

@app.task(bind=True, name='optimise_route')
def optimise_route(self, trip: Dict):
    logger.info(f"Received trip: {trip}")

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

    url: str = settings.C2H["C2H_UPDATE_ROUTE_API"].replace("<id>", str(trip_route["tripId"]))
    headers: Dict = {"Content-Type": "application/json"}
    r: requests.Response = requests.post(url, data=json.dumps(trip_route), headers=headers, verify=False)