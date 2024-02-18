import numpy as np
from typing import AnyStr, Tuple, Any, Dict
from .element import Element
from .coord import auto_coordinates
import pickle as pkl

class Grid:
    def __init__(self, name: AnyStr, size: Tuple[int, int, int]):
        self.grid_name = name
        self.grid = np.empty(size, dtype=object)
        self.grid.fill(None)
        self.size = size
        self._neighbors_offsets = [
            (1, 0, 0), (-1, 0, 0), (0, 1, 0),
            (0, -1, 0), (0, 0, 1), (0, 0, -1)
        ]

    def genesis(self):
        self.add("Genesis Element", {"grid_name": self.grid_name, "size": self.size}, coordinates=(0,0,0))
    def cache(self):
        self.add("Cache Element", dict({}), coordinates=(0,0,1), hash=False)
    def add(self, name: AnyStr, data: Any, coordinates: Tuple[int, int, int]=None, hash: bool=True):
        if coordinates is None:
            coordinates = auto_coordinates(self.grid)
        element = Element(name, data, coordinates, self._get_neighbors(coordinates), hash)
        self._add_to_grid(element)
    
    def get_size(self):
        return self.size

    def _add_to_grid(self, element):
        x, y, z = element.get_coordinates()
        self.grid[x, y, z] = element.get()

    def get(self):
        return self.grid

    def _get_neighbors(self, coord):
        neighbors = []
        for offset in self._neighbors_offsets:
            nx, ny, nz = coord[0] + offset[0], coord[1] + offset[1], coord[2] + offset[2]
            if 0 <= nx < self.size[0] and 0 <= ny < self.size[1] and 0 <= nz < self.size[2]:
                if self.grid[nx, ny, nz] is not None:
                    neighbor_element = self.grid[nx, ny, nz]
                    neighbors.append(((nx, ny, nz), neighbor_element))
        return neighbors
    
    def setdata(self, coordinates: Tuple[int, int, int], data: Any):
        self.grid[coordinates]["data"] = data
    
    def setname(self, coordinates: Tuple[int, int, int], name: str):
        self.grid[coordinates]["name"] = name
    
    def sethash(self, coordinates: Tuple[int, int, int], hash: AnyStr):
        self.grid[coordinates]["hash"] = hash
        
    #TODO: Fix speed of execution this function
    def upn_all(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.size[2]):
                    if self.grid(x, y, z) is not None:
                        self.upn((x, y, z))
    
    def upn(self, coord: Tuple[int, int, int]):
        self.grid[coord]["neighbors"] = self._get_neighbors(coord)

    def save(self):
        with open(f"{self.grid_name}.pkl", 'wb') as f:
            pkl.dump(self.grid, f)
    
    def load(self, filename):
        with open(filename, 'rb') as f:
            self.grid = pkl.load(f)
    def setneighbors(self, coordinates: Tuple[int, int, int], neighbors):
        self.grid[coordinates]["neighbors"] = neighbors