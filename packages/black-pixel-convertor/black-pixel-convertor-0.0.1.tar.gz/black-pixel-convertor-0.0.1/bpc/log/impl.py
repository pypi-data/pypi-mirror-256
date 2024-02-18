from logging import getLogger, Logger, Formatter, StreamHandler, INFO, WARNING


class CustomFormatter(Formatter):
    grey = "\x1b[38;20m"
    green = "\x1b[32m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    level_name = "%(levelname)s"
    space = ": "
    message = "%(message)s"

    regrex = level_name + space + message

    FORMATS = {}

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = Formatter(log_fmt)
        return formatter.format(record)


class TimeFormatter(CustomFormatter):
    green = CustomFormatter.green
    regrex = CustomFormatter.regrex
    reset = CustomFormatter.reset

    FORMATS = {
        INFO: green + regrex + reset
    }


class EventFormatter(CustomFormatter):
    green = CustomFormatter.green
    grey = CustomFormatter.grey
    yellow = CustomFormatter.yellow

    level_name = CustomFormatter.level_name
    space = CustomFormatter.space
    message = CustomFormatter.message
    reset = CustomFormatter.reset

    regrex = CustomFormatter.regrex

    FORMATS = {
        INFO: grey + regrex + reset,
        WARNING: yellow + regrex + reset,
    }


def create_logger(name: str, stm_handler: StreamHandler = None) -> Logger:
    logger = getLogger(name)
    logger.setLevel(INFO)
    logger.addHandler(stm_handler)

    return logger


def create_stream_handler(fmt: Formatter) -> StreamHandler:
    stm_handler = StreamHandler()
    stm_handler.setFormatter(fmt)

    return stm_handler


time_formatter = TimeFormatter()
time_handler = create_stream_handler(time_formatter)
time_logger = create_logger("bpc-time-log", time_handler)

event_formatter = EventFormatter()
event_handler = create_stream_handler(event_formatter)
event_logger = create_logger("bpc-event-log", event_handler)
