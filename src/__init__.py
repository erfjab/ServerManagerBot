import logging


class CustomFormatter(logging.Formatter):
    def format(self, record):
        formatted = super().format(record)
        levelname_with_colon = f"{record.levelname}:"
        return formatted.replace(record.levelname, f"{levelname_with_colon:<9}")


logging.basicConfig(format="[{asctime}] {levelname} {message}", style="{", datefmt="%m/%d %H:%M:%S", level=logging.INFO)

for handler in logging.root.handlers:
    handler.setFormatter(CustomFormatter(fmt="[{asctime}] {levelname} {message}", datefmt="%m/%d %H:%M:%S", style="{"))

logging.getLogger("httpx").propagate = False
