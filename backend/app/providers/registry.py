from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


from app.core.config import get_settings
from app.core.errors import SiteError
from app.providers.anthropic import AnthropicProvider
from app.providers.base import BaseProvider
from app.providers.gemini import GeminiProvider
from app.providers.openai_compat import OpenAICompatibleProvider


@dataclass
class ModelInfo:
    id: str
    name: str
    provider: str
    provider_label: str
    description: str = ""
    context_window: str = ""
    requires_key: bool = True
    free: bool = False


@dataclass
class ProviderMeta:
    id: str
    label: str
    kind: str = "openai_compat"
    env_key: str = ""
    base_url_env: str = ""
    default_base_url: str = ""
    requires_key: bool = True
    tier: str = "free"  # free | paid | local | free+paid
    signup_url: str = ""
    note: str = ""
    tags: list[str] = field(default_factory=list)


PROVIDER_META: list[ProviderMeta] = [
    ProviderMeta(
        id="gemini",
        label="Google Gemini (AI Studio)",
        kind="gemini",
        env_key="GEMINI_API_KEY",
        base_url_env="GEMINI_BASE_URL",
        default_base_url="https://generativelanguage.googleapis.com/v1beta",
        tier="free",
        signup_url="https://aistudio.google.com/apikey",
        note="Free tier with no credit card. Generous flash quotas and 1M context.",
        tags=["free", "multimodal", "long-context"],
    ),
    ProviderMeta(
        id="groq",
        label="Groq",
        env_key="GROQ_API_KEY",
        base_url_env="GROQ_BASE_URL",
        default_base_url="https://api.groq.com/openai/v1",
        tier="free",
        signup_url="https://console.groq.com/keys",
        note="Free developer tier. Extremely fast LPU inference for Llama, Qwen and Kimi.",
        tags=["free", "fastest"],
    ),
    ProviderMeta(
        id="opencode_zen",
        label="OpenCode Zen",
        env_key="OPENCODE_ZEN_API_KEY",
        base_url_env="OPENCODE_ZEN_BASE_URL",
        default_base_url="https://opencode.ai/zen/v1",
        tier="free",
        signup_url="https://opencode.ai/zen",
        note="Curated free coding gateway. OpenAI-compatible, no credit card.",
        tags=["free", "coding"],
    ),
    ProviderMeta(
        id="cerebras",
        label="Cerebras",
        env_key="CEREBRAS_API_KEY",
        base_url_env="CEREBRAS_BASE_URL",
        default_base_url="https://api.cerebras.ai/v1",
        tier="free",
        signup_url="https://cloud.cerebras.ai/",
        note="Free developer tier with very high token throughput.",
        tags=["free", "fastest"],
    ),
    ProviderMeta(
        id="openrouter",
        label="OpenRouter",
        env_key="OPENROUTER_API_KEY",
        base_url_env="OPENROUTER_BASE_URL",
        default_base_url="https://openrouter.ai/api/v1",
        tier="free+paid",
        signup_url="https://openrouter.ai/keys",
        note="Any model from one key. Free models use the ':free' suffix.",
        tags=["free", "multi-model", "aggregator"],
    ),
    ProviderMeta(
        id="nvidia",
        label="NVIDIA NIM",
        env_key="NVIDIA_API_KEY",
        base_url_env="NVIDIA_BASE_URL",
        default_base_url="https://integrate.api.nvidia.com/v1",
        tier="free",
        signup_url="https://build.nvidia.com/",
        note="Free credits and rate-limited endpoints for accelerated open models.",
        tags=["free", "open-weights"],
    ),
    ProviderMeta(
        id="zai",
        label="Z.ai (GLM)",
        env_key="ZAI_API_KEY",
        base_url_env="ZAI_BASE_URL",
        default_base_url="https://api.z.ai/api/paas/v4",
        tier="free",
        signup_url="https://z.ai/manage-apikey/apikey-list",
        note="GLM flash models are permanently free with a signup bonus.",
        tags=["free", "long-context"],
    ),
    ProviderMeta(
        id="siliconflow",
        label="SiliconFlow",
        env_key="SILICONFLOW_API_KEY",
        base_url_env="SILICONFLOW_BASE_URL",
        default_base_url="https://api.siliconflow.cn/v1",
        tier="free",
        signup_url="https://cloud.siliconflow.cn/account/ak",
        note="Dozens of open models at zero cost.",
        tags=["free", "open-weights"],
    ),
    ProviderMeta(
        id="cloudflare",
        label="Cloudflare Workers AI",
        env_key="CLOUDFLARE_API_KEY",
        base_url_env="CLOUDFLARE_BASE_URL",
        default_base_url="https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT_ID/ai/run/v1",
        tier="free",
        signup_url="https://dash.cloudflare.com/?tab=AI",
        note="10k neurons/day free. Replace YOUR_ACCOUNT_ID in the base URL with your account id.",
        tags=["free", "edge"],
    ),
    ProviderMeta(
        id="mistral",
        label="Mistral AI",
        env_key="MISTRAL_API_KEY",
        base_url_env="MISTRAL_BASE_URL",
        default_base_url="https://api.mistral.ai/v1",
        tier="free+paid",
        signup_url="https://console.mistral.ai/api-keys",
        note="Free tier on small models; Codestral handles fill-in-the-middle.",
        tags=["free", "eu-hosted", "coding"],
    ),
    ProviderMeta(
        id="openai",
        label="OpenAI",
        env_key="OPENAI_API_KEY",
        base_url_env="OPENAI_BASE_URL",
        default_base_url="https://api.openai.com/v1",
        tier="paid",
        signup_url="https://platform.openai.com/api-keys",
        note="Broadest tool support and the strongest structured-output guarantees.",
        tags=["paid", "tools", "json-mode"],
    ),
    ProviderMeta(
        id="anthropic",
        label="Anthropic",
        kind="anthropic",
        env_key="ANTHROPIC_API_KEY",
        default_base_url="https://api.anthropic.com/v1",
        tier="paid",
        signup_url="https://console.anthropic.com/settings/keys",
        note="Long-context reasoning models with strong instruction following.",
        tags=["paid", "long-context"],
    ),
    ProviderMeta(
        id="xai",
        label="xAI Grok",
        env_key="XAI_API_KEY",
        base_url_env="XAI_BASE_URL",
        default_base_url="https://api.x.ai/v1",
        tier="paid",
        signup_url="https://console.x.ai/",
        note="Grok flagship and coding models.",
        tags=["paid", "coding"],
    ),
    ProviderMeta(
        id="deepseek",
        label="DeepSeek",
        env_key="DEEPSEEK_API_KEY",
        base_url_env="DEEPSEEK_BASE_URL",
        default_base_url="https://api.deepseek.com/v1",
        tier="paid",
        signup_url="https://platform.deepseek.com/api_keys",
        note="Strong reasoning (deepseek-reasoner) and cheap chat models.",
        tags=["paid", "reasoning"],
    ),
    ProviderMeta(
        id="together",
        label="Together AI",
        env_key="TOGETHER_API_KEY",
        base_url_env="TOGETHER_BASE_URL",
        default_base_url="https://api.together.xyz/v1",
        tier="free+paid",
        signup_url="https://api.together.ai/settings/api-keys",
        note="Sign-up credits for open models and fast inference endpoints.",
        tags=["credits", "open-weights"],
    ),
    ProviderMeta(
        id="fireworks",
        label="Fireworks AI",
        env_key="FIREWORKS_API_KEY",
        base_url_env="FIREWORKS_BASE_URL",
        default_base_url="https://api.fireworks.ai/inference/v1",
        tier="free+paid",
        signup_url="https://fireworks.ai/api-keys",
        note="Optimized open-model serving with function calling.",
        tags=["credits", "open-weights"],
    ),
    ProviderMeta(
        id="ollama",
        label="Ollama (local)",
        env_key="",
        base_url_env="OLLAMA_BASE_URL",
        default_base_url="http://localhost:11434/v1",
        requires_key=False,
        tier="local",
        signup_url="https://ollama.com/download",
        note="Run models on your own machine. Unlimited and private.",
        tags=["local", "offline", "free"],
    ),
    ProviderMeta(
        id="lmstudio",
        label="LM Studio (local)",
        env_key="",
        base_url_env="LMSTUDIO_BASE_URL",
        default_base_url="http://localhost:1234/v1",
        requires_key=False,
        tier="local",
        signup_url="https://lmstudio.ai/",
        note="Local OpenAI-compatible server from the LM Studio app.",
        tags=["local", "offline", "free"],
    ),
    ProviderMeta(
        id="custom",
        label="Custom OpenAI-compatible endpoint",
        env_key="CUSTOM_API_KEY",
        base_url_env="CUSTOM_BASE_URL",
        default_base_url="",
        tier="free+paid",
        signup_url="",
        note="Any gateway that speaks /v1/chat/completions. Set the base URL and key yourself.",
        tags=["custom"],
    ),
]


CURATED_MODELS: list[ModelInfo] = [
    # ---- Gemini (free tier) ----
    ModelInfo("gemini-3.8-flash", "Gemini 3.8 Flash", "gemini", "Google Gemini", "Fast multimodal - free tier.", "1M", free=True),
    ModelInfo("gemini-3.8-flash-lite", "Gemini 3.8 Flash Lite", "gemini", "Google Gemini", "Cheapest fast multimodal - free tier.", "1M", free=True),
    ModelInfo("gemini-3-flash", "Gemini 3 Flash", "gemini", "Google Gemini", "Balanced flash model - free tier.", "1M", free=True),
    ModelInfo("gemini-flash-latest", "Gemini Flash (latest)", "gemini", "Google Gemini", "Auto-updating flash alias - free tier.", "1M", free=True),
    ModelInfo("gemini-3.1-pro-preview", "Gemini 3.1 Pro", "gemini", "Google Gemini", "Deep reasoning - free tier preview.", "1M", free=True),
    # ---- Groq (free tier) ----
    ModelInfo("llama-3.3-70b-versatile", "Llama 3.3 70B", "groq", "Groq", "Fast and capable - free tier.", "128K", free=True),
    ModelInfo("llama-3.1-8b-instant", "Llama 3.1 8B", "groq", "Groq", "Fast small model - free tier.", "128K", free=True),
    ModelInfo("llama-4-scout-17b-16e-instruct", "Llama 4 Scout", "groq", "Groq", "MoE model - free tier.", "128K", free=True),
    ModelInfo("qwen3-32b", "Qwen3 32B", "groq", "Groq", "Strong open model - free tier.", "128K", free=True),
    ModelInfo("kimi-k2-instruct", "Kimi K2", "groq", "Groq", "Agentic model - free tier.", "128K", free=True),
    ModelInfo("gpt-oss-20b", "GPT-OSS 20B", "groq", "Groq", "Open-weight reasoning - free tier.", "128K", free=True),
    # ---- OpenCode Zen (free) ----
    ModelInfo("minimax-m2.5-free", "MiniMax M2.5", "opencode_zen", "OpenCode Zen", "High SWE-bench coding model - free.", "200K", free=True),
    ModelInfo("deepseek-v4-flash-free", "DeepSeek V4 Flash", "opencode_zen", "OpenCode Zen", "Fast general model - free.", "128K", free=True),
    ModelInfo("mimo-v2.5-pro-free", "MiMo V2.5 Pro", "opencode_zen", "OpenCode Zen", "Reasoning model - free.", "128K", free=True),
    ModelInfo("mimo-v2.5-omni-free", "MiMo V2.5 Omni", "opencode_zen", "OpenCode Zen", "Omni-modal model - free.", "128K", free=True),
    ModelInfo("mimo-v2.5-flash-free", "MiMo V2.5 Flash", "opencode_zen", "OpenCode Zen", "Low-latency model - free.", "128K", free=True),
    ModelInfo("nemotron-3-ultra-free", "Nemotron 3 Ultra", "opencode_zen", "OpenCode Zen", "Agentic model - free.", "128K", free=True),
    ModelInfo("nemotron-3-super-free", "Nemotron 3 Super", "opencode_zen", "OpenCode Zen", "Balanced model - free.", "128K", free=True),
    ModelInfo("qwen-3.6-plus-free", "Qwen 3.6 Plus", "opencode_zen", "OpenCode Zen", "Flagship open model - free.", "256K", free=True),
    ModelInfo("trinity-large-preview-free", "Trinity Large Preview", "opencode_zen", "OpenCode Zen", "Preview model - free.", "128K", free=True),
    ModelInfo("north-mini-code-free", "North Mini Code", "opencode_zen", "OpenCode Zen", "Small coding model - free.", "128K", free=True),
    # ---- Cerebras (free tier) ----
    ModelInfo("llama-3.3-70b", "Llama 3.3 70B", "cerebras", "Cerebras", "Ultra-fast inference - free tier.", "128K", free=True),
    ModelInfo("llama3.1-8b", "Llama 3.1 8B", "cerebras", "Cerebras", "Small and quick - free tier.", "128K", free=True),
    ModelInfo("qwen3-235b-a22b-instruct", "Qwen3 235B", "cerebras", "Cerebras", "Huge MoE - free tier.", "128K", free=True),
    ModelInfo("gpt-oss-120b", "GPT-OSS 120B", "cerebras", "Cerebras", "Open-weight reasoning - free tier.", "128K", free=True),
    # ---- OpenRouter (free + paid) ----
    ModelInfo("qwen/qwen3.6-plus:free", "Qwen 3.6 Plus", "openrouter", "OpenRouter", "Free tier via OpenRouter.", "256K", free=True),
    ModelInfo("qwen/qwen3-coder-480b:free", "Qwen3 Coder 480B", "openrouter", "OpenRouter", "Free coding model.", "256K", free=True),
    ModelInfo("mistralai/mistral-small-3.1-24b-instruct:free", "Mistral Small 3.1", "openrouter", "OpenRouter", "Free tier.", "128K", free=True),
    ModelInfo("deepseek/deepseek-chat:free", "DeepSeek V3", "openrouter", "OpenRouter", "Free tier.", "64K", free=True),
    ModelInfo("meta-llama/llama-3.3-70b-instruct:free", "Llama 3.3 70B", "openrouter", "OpenRouter", "Free tier.", "128K", free=True),
    ModelInfo("anthropic/claude-sonnet-4.5", "Claude Sonnet 4.5", "openrouter", "OpenRouter", "Paid tier via OpenRouter.", "200K"),
    ModelInfo("openai/gpt-4o-mini", "GPT-4o mini", "openrouter", "OpenRouter", "Paid tier via OpenRouter.", "128K"),
    # ---- NVIDIA NIM (free) ----
    ModelInfo("meta/llama-3.3-70b-instruct", "Llama 3.3 70B", "nvidia", "NVIDIA NIM", "Accelerated endpoint - free credits.", "128K", free=True),
    ModelInfo("qwen/qwen3-235b-a22b-instruct", "Qwen3 235B", "nvidia", "NVIDIA NIM", "MoE endpoint - free credits.", "128K", free=True),
    ModelInfo("deepseek-ai/deepseek-r1", "DeepSeek R1", "nvidia", "NVIDIA NIM", "Reasoning model - free credits.", "128K", free=True),
    ModelInfo("mistralai/mistral-large-2411", "Mistral Large", "nvidia", "NVIDIA NIM", "Open model - free credits.", "128K", free=True),
    # ---- Z.ai (free) ----
    ModelInfo("glm-4.7-flash", "GLM 4.7 Flash", "zai", "Z.ai", "Permanently free flash model.", "200K", free=True),
    ModelInfo("glm-4.5-flash", "GLM 4.5 Flash", "zai", "Z.ai", "Free flash model.", "128K", free=True),
    ModelInfo("glm-4-flash", "GLM 4 Flash", "zai", "Z.ai", "Legacy free model.", "128K", free=True),
    # ---- SiliconFlow (free) ----
    ModelInfo("Qwen/Qwen3-32B", "Qwen3 32B", "siliconflow", "SiliconFlow", "Open model at zero cost.", "128K", free=True),
    ModelInfo("deepseek-ai/DeepSeek-V3", "DeepSeek V3", "siliconflow", "SiliconFlow", "Open model at zero cost.", "64K", free=True),
    ModelInfo("THUDM/glm-4-9b-chat", "GLM 4 9B", "siliconflow", "SiliconFlow", "Small open model at zero cost.", "128K", free=True),
    # ---- Cloudflare (free quota) ----
    ModelInfo("@cf/meta/llama-3.3-70b-instruct-fp8-fast", "Llama 3.3 70B", "cloudflare", "Cloudflare Workers AI", "Edge model - free neurons.", "128K", free=True),
    ModelInfo("@cf/google/gemma-3-12b-it", "Gemma 3 12B", "cloudflare", "Cloudflare Workers AI", "Edge model - free neurons.", "128K", free=True),
    ModelInfo("@cf/qwen/qwen3-30b-a3b", "Qwen3 30B A3B", "cloudflare", "Cloudflare Workers AI", "Edge MoE model - free neurons.", "128K", free=True),
    # ---- Mistral ----
    ModelInfo("mistral-large-latest", "Mistral Large", "mistral", "Mistral AI", "Flagship Mistral model.", "128K"),
    ModelInfo("mistral-medium-latest", "Mistral Medium", "mistral", "Mistral AI", "Balanced model.", "128K"),
    ModelInfo("mistral-small-latest", "Mistral Small", "mistral", "Mistral AI", "Small model on the free tier.", "128K", free=True),
    ModelInfo("codestral-latest", "Codestral", "mistral", "Mistral AI", "Fill-in-the-middle code model.", "256K"),
    ModelInfo("open-mistral-nemo", "Mistral Nemo", "mistral", "Mistral AI", "Open-weight model.", "128K", free=True),
    # ---- DeepSeek ----
    ModelInfo("deepseek-chat", "DeepSeek V3", "deepseek", "DeepSeek", "Cheap strong chat model.", "64K"),
    ModelInfo("deepseek-reasoner", "DeepSeek R1", "deepseek", "DeepSeek", "Step-by-step reasoning model.", "64K"),
    # ---- OpenAI ----
    ModelInfo("gpt-4o-mini", "GPT-4o mini", "openai", "OpenAI", "Fast, capable, cost-efficient default.", "128K"),
    ModelInfo("gpt-4o", "GPT-4o", "openai", "OpenAI", "Flagship multimodal model.", "128K"),
    ModelInfo("gpt-4.1", "GPT-4.1", "openai", "OpenAI", "Strong reasoning and coding.", "1M"),
    ModelInfo("gpt-4.1-mini", "GPT-4.1 mini", "openai", "OpenAI", "Lightweight GPT-4.1 variant.", "1M"),
    ModelInfo("o4-mini", "o4 mini", "openai", "OpenAI", "Efficient reasoning model.", "200K"),
    # ---- Anthropic ----
    ModelInfo("claude-sonnet-4-5-20250929", "Claude Sonnet 4.5", "anthropic", "Anthropic", "Balanced intelligence and speed.", "200K"),
    ModelInfo("claude-opus-4-1-20250805", "Claude Opus 4.1", "anthropic", "Anthropic", "Highest capability Claude.", "200K"),
    ModelInfo("claude-3-5-haiku-20241022", "Claude 3.5 Haiku", "anthropic", "Anthropic", "Fast, affordable Claude.", "200K"),
    # ---- xAI ----
    ModelInfo("grok-4", "Grok 4", "xai", "xAI Grok", "xAI flagship model.", "256K"),
    ModelInfo("grok-3", "Grok 3", "xai", "xAI Grok", "Previous-generation Grok.", "131K"),
    ModelInfo("grok-3-mini", "Grok 3 mini", "xai", "xAI Grok", "Fast Grok variant.", "131K"),
    ModelInfo("grok-code-1", "Grok Code Fast 1", "xai", "xAI Grok", "Coding-oriented Grok.", "256K"),
    # ---- Together / Fireworks ----
    ModelInfo("meta-llama/Llama-3.3-70B-Instruct-Turbo", "Llama 3.3 70B Turbo", "together", "Together AI", "Fast open model on credits.", "128K", free=True),
    ModelInfo("deepseek-ai/DeepSeek-V3", "DeepSeek V3", "together", "Together AI", "Open model on credits.", "64K", free=True),
    ModelInfo("Qwen/Qwen2.5-72B-Instruct", "Qwen2.5 72B", "together", "Together AI", "Open model on credits.", "128K", free=True),
    ModelInfo("accounts/fireworks/models/llama-v3p3-70b-instruct", "Llama 3.3 70B", "fireworks", "Fireworks AI", "Optimized open model.", "128K", free=True),
    ModelInfo("accounts/fireworks/models/deepseek-v3", "DeepSeek V3", "fireworks", "Fireworks AI", "Optimized open model.", "64K", free=True),
    # ---- Local ----
    ModelInfo("llama3.2", "Llama 3.2 (local)", "ollama", "Ollama", "Local model via Ollama.", "128K", requires_key=False, free=True),
    ModelInfo("qwen2.5-coder", "Qwen 2.5 Coder (local)", "ollama", "Ollama", "Local coding model.", "32K", requires_key=False, free=True),
    ModelInfo("mistral", "Mistral (local)", "ollama", "Ollama", "Local Mistral model.", "32K", requires_key=False, free=True),
    ModelInfo("gemma3", "Gemma 3 (local)", "ollama", "Ollama", "Local Gemma model.", "128K", requires_key=False, free=True),
]

# Order used when the learner has not pinned a tutor model yet.
DEFAULT_TUTOR_PREFERENCE = [
    ("gemini", "gemini-3.8-flash"),
    ("groq", "llama-3.3-70b-versatile"),
    ("opencode_zen", "mimo-v2.5-pro-free"),
    ("cerebras", "llama-3.3-70b"),
    ("openrouter", "qwen/qwen3.6-plus:free"),
    ("nvidia", "meta/llama-3.3-70b-instruct"),
    ("zai", "glm-4.7-flash"),
    ("siliconflow", "Qwen/Qwen3-32B"),
    ("ollama", "llama3.2"),
    ("openai", "gpt-4o-mini"),
    ("anthropic", "claude-sonnet-4-5-20250929"),
    ("xai", "grok-4"),
    ("deepseek", "deepseek-chat"),
    ("mistral", "mistral-small-latest"),
]


class ProviderRegistry:
    """Resolves credentials from the environment and builds providers.

    The site reads provider status to show which keys are present on this
    machine; nothing is ever persisted or sent to the browser.
    """

    def __init__(self, db: object | None = None) -> None:
        self.settings = get_settings()
        self.db = db

    async def _load_db_config(self) -> dict[str, dict[str, str]]:
        return {}

    async def resolve_key(self, provider_id: str) -> str:
        meta = _meta(provider_id)
        env_value = getattr(self.settings, meta.env_key.lower(), "") if meta.env_key else ""
        return env_value.strip()

    async def resolve_base_url(self, provider_id: str) -> str:
        meta = _meta(provider_id)
        if meta.base_url_env:
            env_value = getattr(self.settings, meta.base_url_env.lower(), "") or ""
            if env_value:
                return env_value.rstrip("/")
        return meta.default_base_url

    async def is_configured(self, provider_id: str) -> bool:
        meta = _meta(provider_id)
        if not meta.requires_key:
            return True
        if provider_id == "custom":
            return bool(await self.resolve_base_url(provider_id))
        return bool(await self.resolve_key(provider_id))

    def _timeout(self) -> int:
        return self.settings.amt_provider_timeout_seconds

    async def get_provider(self, provider_id: str) -> BaseProvider:
        meta = _meta(provider_id)
        key = await self.resolve_key(provider_id)
        base_url = await self.resolve_base_url(provider_id)
        if meta.kind == "anthropic":
            return AnthropicProvider(api_key=key, timeout=self._timeout())
        if meta.kind == "gemini":
            return GeminiProvider(api_key=key, timeout=self._timeout(), base_url=base_url)
        return OpenAICompatibleProvider(
            api_key=key,
            base_url=base_url,
            timeout=self._timeout(),
            name=provider_id,
            label=meta.label,
            require_key=meta.requires_key,
        )

    async def provider_status(self) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for meta in PROVIDER_META:
            configured = await self.is_configured(meta.id)
            env_value = getattr(self.settings, meta.env_key.lower(), "") if meta.env_key else ""
            db_cfg = await self._load_db_config()
            entry = db_cfg.get(meta.id) or {}
            out.append(
                {
                    "id": meta.id,
                    "label": meta.label,
                    "kind": meta.kind,
                    "tier": meta.tier,
                    "tags": meta.tags,
                    "note": meta.note,
                    "signup_url": meta.signup_url,
                    "configured": configured,
                    "requires_key": meta.requires_key,
                    "has_env_key": bool(env_value),
                    "has_stored_key": bool(entry.get("api_key")),
                    "base_url": await self.resolve_base_url(meta.id),
                    "default_base_url": meta.default_base_url,
                }
            )
        return out

    async def configured_provider_ids(self) -> list[str]:
        status = await self.provider_status()
        return [p["id"] for p in status if p["configured"]]

    async def default_tutor_model(self) -> tuple[str, str]:
        """Pick the best available tutor model: configured first, then any free tier."""
        configured = set(await self.configured_provider_ids())
        for provider_id, model_id in DEFAULT_TUTOR_PREFERENCE:
            if provider_id in configured:
                return provider_id, model_id
        # Nothing configured yet - still return a sensible default so the UI has a value.
        return DEFAULT_TUTOR_PREFERENCE[0]

    async def models_for_frontend(self) -> list[dict[str, Any]]:
        status = {p["id"]: p for p in await self.provider_status()}
        models: list[dict[str, Any]] = []
        for m in CURATED_MODELS:
            models.append(
                {
                    "id": m.id,
                    "name": m.name,
                    "provider": m.provider,
                    "provider_label": m.provider_label,
                    "description": m.description,
                    "context_window": m.context_window,
                    "requires_key": m.requires_key,
                    "supports_streaming": True,
                    "configured": status.get(m.provider, {}).get("configured", False),
                    "free": m.free,
                    "tier": status.get(m.provider, {}).get("tier", "free"),
                }
            )
        return models


def _meta(provider_id: str) -> ProviderMeta:
    for m in PROVIDER_META:
        if m.id == provider_id:
            return m
    raise SiteError(f"Unknown provider '{provider_id}'.", code="unknown_provider", status_code=400)


def provider_meta(provider_id: str) -> ProviderMeta:
    return _meta(provider_id)
