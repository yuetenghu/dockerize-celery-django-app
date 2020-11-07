from typing import List
import unittest
import sys
sys.path.append(".")
from held_karp import HeldKarp

class HeldKarpTest(unittest.TestCase):

    dists1: List[List[int]] = [
        [0,  2,  9, 10],
        [1,  0,  6,  4],
        [15, 7,  0,  8],
        [6,  3, 12,  0]
    ]

    dists2: List[List[int]] = [
        [ 0, 49 ,34, 96, 74],
        [49,  0 ,10, 94, 43],
        [34, 10 , 0, 21,  6],
        [96, 94 ,21,  0, 70],
        [74, 43 , 6, 70,  0]
    ]

    def test_tsp_shortest_path(self):
        held_karp = HeldKarp(self.dists1)
        min_cost: int
        path: List[int]
        min_cost, path = held_karp.tsp_shortest_path()
        print(f"Minimum cost: {min_cost}")
        print(f"Shortest_path: {path}")
        self.assertEqual(min_cost, 21)
        self.assertEqual(path, [0, 2, 3, 1, 0])

        held_karp = HeldKarp(self.dists2)
        min_cost: int
        path: List[int]
        min_cost, path = held_karp.tsp_shortest_path()
        print(f"Minimum cost: {min_cost}")
        print(f"Shortest_path: {path}")
        self.assertEqual(min_cost, 215)
        self.assertEqual(path, [0, 3, 2, 4, 1, 0])


if __name__ == "__main__":
    unittest.main()