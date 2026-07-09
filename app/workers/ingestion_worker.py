"""
Ingestion worker.

Background worker responsible for processing document ingestion jobs.
"""

from __future__ import annotations

from queue import Queue
from threading import Thread

from app.core.logging_config import get_logger
from app.pipelines.ingestion_pipeline import (
    ingestion_pipeline,
)

logger = get_logger(__name__)


class IngestionWorker:
    """
    Background ingestion worker.
    """

    def __init__(
        self,
    ) -> None:

        self._queue: Queue[str] = Queue()

        self._thread = Thread(
            target=self._run,
            daemon=True,
        )

        self._running = False

    def start(
        self,
    ) -> None:
        """
        Start the worker.
        """

        if self._running:

            return

        self._running = True

        self._thread.start()

        logger.info(
            "Ingestion worker started."
        )

    def stop(
        self,
    ) -> None:
        """
        Stop the worker.
        """

        self._running = False

        logger.info(
            "Ingestion worker stopped."
        )

    def submit(
        self,
        file_path: str,
    ) -> None:
        """
        Submit a document for ingestion.

        Args:
            file_path:
                Document path.
        """

        self._queue.put(
            file_path,
        )

        logger.info(
            "Queued document for ingestion: %s",
            file_path,
        )

    def _run(
        self,
    ) -> None:
        """
        Worker loop.
        """

        while self._running:

            file_path = self._queue.get()

            try:

                logger.info(
                    "Processing document: %s",
                    file_path,
                )

                ingestion_pipeline.run(
                    file_path=file_path,
                )

                logger.info(
                    "Successfully processed: %s",
                    file_path,
                )

            except Exception:

                logger.exception(
                    "Failed to process document: %s",
                    file_path,
                )

            finally:

                self._queue.task_done()


ingestion_worker = IngestionWorker()