import logging
import logging.handlers
import os
import time
from typing import Callable


class filters:
    @classmethod
    def _util(cls, levels: str | list[str], comparefn: Callable) -> Callable:
        """
        @param levels: 日志级别
        @param comparefn: 一个二元谓词
            1. 实际接收到的日志级别
            2. 外部指定的需要过滤的日志级别
        """
        if isinstance(levels, str) or isinstance(levels, list) and len(levels) == 1:
            levelno = getattr(logging, levels.upper())
        else:
            levelno = [getattr(logging, lv.upper()) for lv in levels]

        def _filter(record: logging.LogRecord):
            return comparefn(record.levelno, levelno)

        return _filter

    @classmethod
    def eq(cls, levels: str) -> bool:
        """equal"""
        return cls._util(levels, lambda a, b: a == b)

    @classmethod
    def ne(cls, levels: str) -> bool:
        """not equal"""
        return cls._util(levels, lambda a, b: a != b)

    @classmethod
    def gt(cls, levels: str) -> bool:
        """greater than"""
        return cls._util(levels, lambda a, b: a > b)

    @classmethod
    def ge(cls, levels: str) -> bool:
        """greater equal"""
        return cls._util(levels, lambda a, b: a >= b)

    @classmethod
    def lt(cls, levels: str) -> bool:
        """less than"""
        return cls._util(levels, lambda a, b: a < b)

    @classmethod
    def le(cls, levels: str) -> bool:
        """less equal"""
        return cls._util(levels, lambda a, b: a <= b)

    @classmethod
    def include(cls, levels: list[str]) -> bool:
        return cls._util(levels, lambda a, b: a in b)

    @classmethod
    def exlude(cls, levels: list[str]) -> bool:
        return cls._util(levels, lambda a, b: a not in b)


class handlers:
    class sized_timed_rotating_file_handler(logging.handlers.BaseRotatingHandler):
        def __init__(
            self,
            filename,
            mode="a+",
            max_bytes=0,
            backup_count=0,
            when="h",
            interval=1,
            utc=False,
            encoding=None,
            delay=False,
            errors=None,
        ):
            super().__init__(filename, mode, encoding, delay, errors)

            # sized rotating parameters
            self.max_bytes = max_bytes
            self.backup_count = backup_count

            # timed rotating parameters
            self.when = when.lower()
            self.interval = interval * self.get_interval_seconds()  # normalize to seconds
            self.utc = utc
            self.next_rollover_at = self.compute_next_rollover()

            # initialize file size
            if os.path.exists(filename):
                self.current_size = os.stat(filename).st_size
            else:
                self.current_size = 0

        def get_interval_seconds(self) -> int:
            intervals = {
                "s": 1,
                "m": 60,
                "h": 60 * 60,
                "d": 60 * 60 * 24,
            }
            return intervals.get(self.when, 60 * 60 * 24)

        def compute_next_rollover(self) -> float:
            # now = time.gmtime() if self.utc else time.time()
            now = time.time()
            return (now // self.interval + 1) * self.interval

        def should_rollover(self, record: logging.LogRecord) -> int:
            if time.time() >= self.next_rollover_at:
                return 1
            elif self.max_bytes > 0 and self.current_size + len(self.format(record).encode()) >= self.max_bytes:
                return 2
            else:
                return 0

        def do_rollover(self, trigger_type: int):
            self.close()

            time_suffix = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
            base = f"{self.baseFilename}.{time_suffix}"

        def emit(self, record):
            return super().emit(record)


if __name__ == "__main__":
    print(time.localtime())
