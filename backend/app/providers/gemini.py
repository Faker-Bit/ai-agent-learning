from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any

import httpx

from app.core.errors import ProviderAuthError, ProviderError
from app.providers.base import BaseProvider, ChatMessage

GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta"


class GeminiProvider(BaseProvider):
    name = "gemini"
    label = "Google Gemini"

    def __init__(self, api_key: str, timeout: int = 120, base_url: str | None = None) -> None:
        super().__init__(api_key=api_key or "", base_url=base_url or GEMINI_BASE, timeout=timeout)

    async def stream_chat(
        self,
        messages: list[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        extra: dict[str, Any] | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        if not self.api_key:
            raise ProviderAuthError(self.name, "Add the Google AI Studio key in Settings -> Providers.")

        system_parts = [m.content for m in messages if m.role == "system"]
        contents = [
            {"role": "user" if m.role == "user" else "model", "parts": [{"text": m.content}]}
            for m in messages
            if m.role in ("user", "assistant")
        ]
        payload: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
        }
        if system_parts:
            payload["systemInstruction"] = {"parts": [{"text": "\n\n".join(system_parts)}]}

        url = f"{self.base_url.rstrip('/')}/models/{model}:streamGenerateContent?alt=sse"
        headers = {"x-goog-api-key": self.api_key, "Content-Type": "application/json"}
        usage: dict[str, Any] = {}
        finish_reason: str | None = None
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(self.timeout, connect=15)) as client:
                async with client.stream("POST", url, headers=headers, json=payload) as resp:
                    if resp.status_code in (401, 403):
                        raise ProviderAuthError(self.name, await _err(resp))
                    if resp.status_code >= 400:
                        raise ProviderError(f"Gemini returned {resp.status_code}: {await _err(resp)}", self.name)
                    async for line in resp.aiter_lines():
                        if not line or not line.startswith("data:"):
                            continue
                        data = line[5:].strip()
                        try:
                            chunk = json.loads(data)
                        except json.JSONDecodeError:
                            continue
                        cand = (chunk.get("candidates") or [{}])[0]
                        parts = (cand.get("content") or {}).get("parts") or []
                        for part in parts:
                            text = part.get("text")
                            if text:
                                yield {"type": "token", "text": text}
                        if cand.get("finishReason"):
                            finish_reason = cand["finishReason"]
                        meta = chunk.get("usageMetadata")
                        if meta:
                            usage = {
                                "prompt_tokens": meta.get("promptTokenCount"),
                                "completion_tokens": meta.get("candidatesTokenCount"),
                                "total_tokens": meta.get("totalTokenCount"),
                            }
        except httpx.TimeoutException:
            raise ProviderError("Gemini request timed out.", self.name)
        except httpx.HTTPError as exc:
            raise ProviderError(f"Network error contacting Gemini: {exc}", self.name)

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
                    headers={"x-goog-api-key": self.api_key},
                )
                if resp.status_code != 200:
                    return []
                data = resp.json()
                names = []
                for m in data.get("models", []):
                    name = m.get("name", "")
                    if name.startswith("models/"):
                        name = name[len("models/") :]
                    if "gemini" in name:
                        names.append(name)
                return names[:60]
        except httpx.HTTPError:
            return []


async def _err(resp: httpx.Response) -> str:
    body = await resp.aread()
    try:
        parsed = json.loads(body)
        err = parsed.get("error") or {}
        return str(err.get("message", ""))[:300]
    except Exception:
        return body.decode("utf-8", errors="replace")[:300]
