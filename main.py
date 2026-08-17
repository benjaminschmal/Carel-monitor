import logging
import threading

import uvicorn

from config import WEB_HOST, WEB_PORT
from core.scanner import Scanner
from database import init_database


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


def run_web_server() -> None:
    uvicorn.run(
        "app:app",
        host=WEB_HOST,
        port=WEB_PORT,
        log_level="info",
    )


def main() -> None:
    init_database()

    web_thread = threading.Thread(
        target=run_web_server,
        daemon=True,
        name="web-server",
    )
    web_thread.start()

    scanner = Scanner()

    try:
        scanner.run()
    except KeyboardInterrupt:
        logger.info("CAREL Monitor stopped")
    except Exception:
        logger.exception("CAREL Monitor stopped due to an unexpected error")
        raise


if __name__ == "__main__":
    main()
