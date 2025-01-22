import abc


class Options(abc.ABC):
    pass


class Proxy(abc.ABC):
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def close(self):
        pass

    @abc.abstractmethod
    def commit(self):
        pass

    @abc.abstractmethod
    def execute(self, sqltext: str, params: tuple = None):
        pass

    @abc.abstractmethod
    def executescript(self, sqltext: str):
        pass

    def get_options(self) -> Options:
        return self._options

    def get_conn(self):
        if self._conn is None:
            self.connect()
        return self._conn
