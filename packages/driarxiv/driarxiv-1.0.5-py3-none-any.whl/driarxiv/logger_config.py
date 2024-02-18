import logging


# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    handlers=[
                        logging.FileHandler("driarxiv.log"),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)