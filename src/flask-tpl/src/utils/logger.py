import logging
import logging.config
import typing


class Logger:
    Config: typing.TypeAlias = typing.Union[typing.Mapping, str, None]
    ConfigMap: typing.TypeAlias = typing.Dict[str, typing.Any]
    LogLevel: typing.TypeAlias = typing.Union[int, str]

    DEFAULT_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s %(module)s.%(funcName)s:%(lineno)d %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }

    def __init__(self, name: str = __name__, config: Config = None) -> None:
        """
        - name: the name of the logger
        - config: the logging configuration, can be a mapping or a string representing a file path(json/toml format), or None to use the default configuration
        """
        self._logger = logging.getLogger(name)
        self._configure(config)

    def _configure(self, config: Config) -> None:
        logging.config.dictConfig(self._load_config(config))

    def _load_config(self, config: Config) -> ConfigMap:
        if isinstance(config, typing.Mapping):
            return config
        elif isinstance(config, str):
            raise NotImplementedError
        else:
            return self.DEFAULT_CONFIG

    def add_handler(self, handler: logging.Handler) -> None:
        self._logger.addHandler(handler)

    def set_level(self, level: LogLevel) -> None:
        self._logger.setLevel(level)

    def log(self, level: LogLevel, msg: str, **kwargs) -> None:
        self._logger.log(level, msg, **kwargs)

    def debug(self, msg: str, **kwargs) -> None:
        self._logger.debug(msg, **kwargs)

    def info(self, msg: str, **kwargs) -> None:
        self._logger.info(msg, **kwargs)

    def warning(self, msg: str, **kwargs) -> None:
        self._logger.warning(msg, **kwargs)

    def error(self, msg: str, **kwargs) -> None:
        self._logger.error(msg, exc_info=True, **kwargs)

    # def exception(self, msg: str, **kwargs) -> None:
    #     self._logger.exception(msg, **kwargs)

    def critical(self, msg: str, **kwargs) -> None:
        self._logger.critical(msg, exc_info=True, **kwargs)


if __name__ == "__main__":
    log = Logger()
    log.info("Hello, world!")

    try:
        1 / 0
    except Exception as e:
        log.error(e)
