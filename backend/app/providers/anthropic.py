from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any

import httpx

from app.core.errors import ProviderAuthError, ProviderError
from app.providers.base import BaseProvider, ChatMessage

ANTHROPIC_API_URL = "https://api.anthropic.com/v1"
ANTHROPIC_VERSION = "2023-06-01"


class AnthropicProvider(BaseProvider):
    name = "anthropic"
    label = "Anthropic"

    def __init__(self, api_key: str, timeout: int = 120, base_url: str | None = None) -> None:
        super().__init__(api_key=api_key or "", base_url=base_url or ANTHROPIC_API_URL, timeout=timeout)

    async def stream_chat(
        self,
        messages: list[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        extra: dict[str, Any] | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        if not self.api_key:
            raise ProviderAuthError(self.name, "Add the Anthropic API key in Settings -> Providers.")

        system_parts = [m.content for m in messages if m.role == "system"]
        chat = [m for m in messages if m.role in ("user", "assistant")]
        payload: dict[str, Any] = {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in chat],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True,
        }
        if system_parts:
            payload["system"] = "\n\n".join(system_parts)

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": ANTHROPIC_VERSION,
            "content-type": "application/json",
        }
        url = f"{self.base_url.rstrip('/')}/messages"
        usage: dict[str, Any] = {}
        finish_reason: str | None = None
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(self.timeout, connect=15)) as client:
                async with client.stream("POST", url, headers=headers, json=payload) as resp:
                    if resp.status_code in (401, 403):
                        raise ProviderAuthError(self.name, await _read_error(resp))
                    if resp.status_code >= 400:
                        raise ProviderError(
                            f"Anthropic returned {resp.status_code}: {await _read_error(resp)}", self.name
                        )
                    async for line in resp.aiter_lines():
                        if not line or not line.startswith("data:"):
                            continue
                        data = line[5:].strip()
                        try:
                            event = json.loads(data)
                        except json.JSONDecodeError:
                            continue
                        etype = event.get("type")
                        if etype == "content_block_delta":
                            delta = event.get("delta") or {}
                            if delta.get("type") == "text_delta" and delta.get("text"):
                                yield {"type": "token", "text": delta["text"]}
                        elif etype == "message_delta":
                            delta = event.get("delta") or {}
                            if delta.get("stop_reason"):
                                finish_reason = delta["stop_reason"]
                            u = event.get("usage")
                            if u:
                                usage = {**usage, **u}
                        elif etype == "message_start":
                            u = (event.get("message") or {}).get("usage")
                            if u:
                                usage = {**u, **usage}
                        elif etype == "error":
                            err = event.get("error") or {}
                            raise ProviderError(err.get("message") or "Anthropic stream error.", self.name)
        except httpx.TimeoutException:
            raise ProviderError("Anthropic request timed out.", self.name)
        except httpx.HTTPError as exc:
            raise ProviderError(f"Network error contacting Anthropic: {exc}", self.name)

        if usage:
            yield {"type": "usage", "usage": usage}
        yield {"type": "done", "finish_reason": finish_reason}

    async def list_models(self) -> list[str]:
        if not self.api_key:
            return []
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{self.base_url.rstrip('/')}/models",
                    headers={"x-api-key": self.api_key, "anthropic-version": ANTHROPIC_VERSION},
                )
                if resp.status_code != 200:
                    return []
                data = resp.json()
                return [m.get("id", "") for m in data.get("data", []) if m.get("id")][:50]
        except httpx.HTTPError:
            return []


async def _read_error(resp: httpx.Response) -> str:
    body = await resp.aread()
    try:
        parsed = json.loads(body)
        err = parsed.get("error")
        if isinstance(err, dict):
            return str(err.get("message", ""))[:300]
    except Exception:
        pass
    return body.decode("utf-8", errors="replace")[:300]
