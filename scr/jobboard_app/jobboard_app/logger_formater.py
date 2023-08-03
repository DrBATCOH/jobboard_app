import logging


class ContextFormatter(logging.Formatter):
    def format(self, log_record: logging.LogRecord) -> str:
        formatted_message = super().format(record=log_record)
        return formatted_message