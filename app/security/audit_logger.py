"""
Audit logger.

Provides centralized security audit logging for authentication,
authorization, and other security-sensitive events.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from app.core.config.settings import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


class AuditLogger:
    """
    Security audit logger.

    Every security-sensitive action should be logged through this class.
    """

    def __init__(self) -> None:

        self._log_file = Path(
            settings.audit_log_path,
        )

        self._log_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def log_event(
        self,
        event: str,
        username: str | None = None,
        status: str = "SUCCESS",
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Write an audit event.

        Args:
            event:
                Event name.

            username:
                User performing the action.

            status:
                SUCCESS / FAILED.

            details:
                Additional metadata.
        """

        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "username": username,
            "status": status,
            "details": details or {},
        }

        with self._log_file.open(
            mode="a",
            encoding="utf-8",
        ) as file:

            file.write(
                json.dumps(record)
            )

            file.write("\n")

        logger.info(
            "Audit event recorded: %s",
            event,
        )

    def login_success(
        self,
        username: str,
    ) -> None:
        """
        Log successful authentication.
        """

        self.log_event(
            event="LOGIN",
            username=username,
            status="SUCCESS",
        )

    def login_failed(
        self,
        username: str,
    ) -> None:
        """
        Log failed authentication.
        """

        self.log_event(
            event="LOGIN",
            username=username,
            status="FAILED",
        )

    def document_uploaded(
        self,
        username: str,
        filename: str,
    ) -> None:
        """
        Log document upload.
        """

        self.log_event(
            event="DOCUMENT_UPLOAD",
            username=username,
            details={
                "filename": filename,
            },
        )

    def document_deleted(
        self,
        username: str,
        filename: str,
    ) -> None:
        """
        Log document deletion.
        """

        self.log_event(
            event="DOCUMENT_DELETE",
            username=username,
            details={
                "filename": filename,
            },
        )

    def search_query(
        self,
        username: str,
        query: str,
    ) -> None:
        """
        Log search activity.
        """

        self.log_event(
            event="SEARCH",
            username=username,
            details={
                "query": query,
            },
        )

    def chat_request(
        self,
        username: str,
        question: str,
    ) -> None:
        """
        Log chat request.
        """

        self.log_event(
            event="CHAT",
            username=username,
            details={
                "question": question,
            },
        )


audit_logger = AuditLogger()