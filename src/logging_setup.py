import logging


def logging_setup(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="[%(asctime)s] %(levelname)s - %(name)s : %(message)s",
        filename="logging.log",
    )

    console = logging.StreamHandler()
    logging.getLogger("rackscribe").addHandler(console)
