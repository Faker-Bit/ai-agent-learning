from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any

import httpx

from app.core.errors import ProviderAuthError, ProviderError
from app.providers.base import BaseProvider, ChatMessage


class OpenAICompatibleProvider(BaseProvider):
    """Adapter for OpenAI-compatible Chat Completions APIs.

    Covers OpenAI, xAI, Groq, Cerebras, OpenRouter, OpenCode Zen, NVIDIA NIM,
    Z.ai, SiliconFlow, Mistral, DeepSeek, Together, Fireworks, Cloudflare
    Workers AI, Ollama, LM Studio and any custom OpenAI-compatible gateway.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: int = 120,
        name: str = "openai",
        label: str = "OpenAI",
        require_key: bool = True,
    ) -> None:
        super().__init__(api_key=api_key or "", base_url=base_url, timeout=timeout)
        self.name = name
        self.label = label
        self.require_key = require_key

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def stream_chat(
        self,
        messages: list[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        extra: dict[str, Any] | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        if self.require_key and not self.api_key:
            raise ProviderAuthError(self.name, "Add the API key in Settings -> Providers.")
        if not self.base_url:
            raise ProviderError(
                f"{self.label} has no base URL configured. Set one in Settings -> Providers.",
                self.name,
            )

        payload: dict[str, Any] = {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
            "stream_options": {"include_usage": True},
        }
        if extra:
            effort = extra.get("reasoning_effort")
            if effort and effort in ("low", "medium", "high"):
                payload["reasoning_effort"] = effort
            if extra.get("json_mode"):
                payload["response_format"] = {"type": "json_object"}
            if extra.get("stop"):
                payload["stop"] = extra["stop"]

        url = f"{self.base_url}/chat/completions"
        usage: dict[str, Any] = {}
        finish_reason: str | None = None
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(self.timeout, connect=15)) as client:
                async with client.stream("POST", url, headers=self._headers(), json=payload) as resp:
                    if resp.status_code in (401, 403):
                        body = await resp.aread()
                        raise ProviderAuthError(self.name, _safe_body(body))
                    if resp.status_code == 429:
                        body = await resp.aread()
                        raise ProviderError(f"Rate limited by {self.label}: {_safe_body(body)}", self.name)
                    if resp.status_code >= 400:
                        body = await resp.aread()
                        raise ProviderError(
                            f"{self.label} returned {resp.status_code}: {_safe_body(body)}", self.name
                        )
                    async for line in resp.aiter_lines():
                        if not line or not line.startswith("data:"):
                            continue
                        data = line[5:].strip()
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                        except json.JSONDecodeError:
                            continue
                        if chunk.get("usage"):
                            usage = chunk["usage"]
                        if chunk.get("error"):
                            err = chunk["error"]
                            msg = err.get("message") if isinstance(err, dict) else str(err)
                            raise ProviderError(f"{self.label}: {msg}", self.name)
                        choices = chunk.get("choices") or []
                        if not choices:
                            continue
                        choice = choices[0]
                        delta = choice.get("delta") or {}
                        content = delta.get("content")
                        if isinstance(content, list):
                            content = "".join(part.get("text", "") for part in content if isinstance(part, dict))
                        if content:
                            yield {"type": "token", "text": content}
                        if choice.get("finish_reason"):
                            finish_reason = choice["finish_reason"]
        except httpx.TimeoutException:
            raise ProviderError(f"{self.label} request timed out.", self.name)
        except httpx.HTTPError as exc:
            raise ProviderError(f"Network error contacting {self.label}: {exc}", self.name)

        if usage:
            yield {"type": "usage", "usage": usage}
        yield {"type": "done", "finish_reason": finish_reason}

    async def list_models(self) -> list[str]:
        if not self.base_url:
            return []
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(f"{self.base_url}/models", headers=self._headers())
                if resp.status_code != 200:
                    return []
                data = resp.json()
                items = data.get("data") or []
                return [m.get("id", "") for m in items if m.get("id")][:120]
        except httpx.HTTPError:
            return []


def _safe_body(body: bytes, limit: int = 300) -> str:
    try:
        text = body.decode("utf-8", errors="replace")
    except Exception:
        return "(unreadable error body)"
    try:
        parsed = json.loads(text)
        err = parsed.get("error")
        if isinstance(err, dict):
            text = err.get("message") or text
        elif isinstance(err, str):
            text = err
    except Exception:
        pass
    return text[:limit]
