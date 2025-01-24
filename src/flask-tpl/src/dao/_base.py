import abc

from src.db import get_db


class AbstractDao(abc.ABC):
    def __init__(self):
        super().__init__()

        self.proxy = get_db()
