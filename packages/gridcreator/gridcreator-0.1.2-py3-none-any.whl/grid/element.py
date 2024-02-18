from typing import AnyStr, Tuple, Any
import numpy as np
import hashlib
class Element:
    def __init__(self, name: AnyStr, data: Any, coordinates: Tuple[int, int, int], neighbors: np.ndarray, hash=True):
        self.name = name
        self.data = data
        self.coordinates = coordinates
        self.neighbors = neighbors
        self.hash = None
        if hash:
            self.hash = self._gen_hash(str(self.data))
    
    def get_data(self) -> Any:
        return self.data
    
    def get_name(self) -> AnyStr:
        return self.name
    
    def _gen_hash(self, data: AnyStr) -> str:
        return hashlib.sha256(data.encode("utf-8")).hexdigest()
    
    def get_coordinates(self) -> Tuple[int, int, int]:
        return self.coordinates
    
    def get_hash(self) -> AnyStr:
        return self.hash
    
    def get_neighbors(self) -> np.ndarray:
        return self.neighbors
    
    def get(self) -> dict:
        return {"name": self.name, "hash": self.hash, "coordinates": self.coordinates, "data": self.data, "neighbors": self.neighbors}
