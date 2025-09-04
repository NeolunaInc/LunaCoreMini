import logging
import os

# Configuration simple du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('lunacore')

def info(msg, category="general"):
    logger.info(f"[{category.upper()}] {msg}")

def warning(msg, category="general"):
    logger.warning(f"[{category.upper()}] {msg}")

def error(msg, category="general"):
    logger.error(f"[{category.upper()}] {msg}")

def success(msg, category="general"):
    logger.info(f"[SUCCESS] {msg}")

def get_logger():
    return logger
