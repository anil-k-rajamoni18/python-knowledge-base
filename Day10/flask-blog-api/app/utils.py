# app/utils.py
from flask import current_app
from datetime import datetime
import logging

def paginate_query(query, page, per_page):
    page = max(1, int(page or 1))
    per_page = int(per_page or current_app.config.get("POSTS_PER_PAGE", 10))
    items = query.limit(per_page).offset((page-1)*per_page).all()
    return items

def log_event(message, level="info"):
    logger = logging.getLogger("app")
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    else:
        logger.debug(message)
