import logging
from interface.cli import run_cli
from config import load_config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    try:
        config = load_config()
        if config:
            run_cli(config)
        else:
            logger.error("Failed to load configuration.")
    except Exception as e:
        logger.exception(f"An error occurred in main: {e}")

if __name__ == "__main__":
    main()
