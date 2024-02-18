from .route import Route
from ..enums import HTTPMethodType

class Head(Route):
    def __init__(self, path: str):
        super().__init__(path, HTTPMethodType.HEAD)