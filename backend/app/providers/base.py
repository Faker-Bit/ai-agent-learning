from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ChatMessage:
    role: str  # system | user | assistant
    content: str


@dataclass
class ProviderResult:
    """Final aggregated stream result."""

    text: str = ""
    usage: dict[str, Any] = field(default_factory=dict)
    finish_reason: str | None = None
    model: str | None = None


class BaseProvider(ABC):
    """Provider-independent chat adapter.

    Implementations must yield `dict` events:
      {"type": "token", "text": str}
      {"type": "usage", "usage": dict}
      {"type": "done", "finish_reason": str|None}
      {"type": "error", "message": str, "code": str}
    """

    name: str = "base"
    label: str = "Base"

    def __init__(self, api_key: str, base_url: str | None = None, timeout: int = 120) -> None:
        self.api_key = api_key
        self.base_url = (base_url or "").rstrip("/")
        self.timeout = timeout

    @abstractmethod
    def stream_chat(
        self,
        messages: list[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        extra: dict[str, Any] | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        ...

    @abstractmethod
    async def list_models(self) -> list[str]:
        ...

    async def complete(
        self,
        messages: list[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        extra: dict[str, Any] | None = None,
    ) -> ProviderResult:
        """Non-streaming convenience wrapper used by the judge and graders."""
        chunks: list[str] = []
        usage: dict[str, Any] = {}
        finish_reason: str | None = None
        async for event in self.stream_chat(messages, model, temperature, max_tokens, extra):
            etype = event.get("type")
            if etype == "token":
                chunks.append(str(event.get("text", "")))
            elif etype == "usage":
                usage = dict(event.get("usage") or {})
            elif etype == "done":
                finish_reason = event.get("finish_reason")
        return ProviderResult(
            text="".join(chunks),
            usage=usage,
            finish_reason=finish_reason,
            model=model,
        )
