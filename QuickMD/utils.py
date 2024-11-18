import logging
import os

def setup_logging(log_file: str = 'logs/app.log') -> None:
    """Sets up logging configuration."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        filename=log_file,
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
