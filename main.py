import logging
from interface.cli import run_cli
from config import load_config
import asyncio

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='echomitm.log', filemode='w')
logger = logging.getLogger(__name__)

async def main():
    try:
        config = load_config()
        if config:
            await run_cli(config)
        else:
            logger.error("Failed to load configuration.")
    except Exception as e:
        logger.exception(f"An error occurred in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())
