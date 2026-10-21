from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from app.content.agents import AGENTS
from app.content.cheatsheet import CHEATSHEET, cheatsheet_groups
from app.content.guide import (
    CRAFT,
    LOOP_STAGES,
    MODEL_GUIDE,
    CONFIG_SNIPPETS,
    comparison_matrix,
)
from app.content.harness import (
    CONTEXT_PLAYBOOK,
    HARNESS_LAYERS,
    HARNESS_PROJECTS,
    ORCHESTRATORS,
    PROTOCOLS,
    SKILL_FORMAT,
    SKILL_PACKAGES,
)
from app.content.walkthroughs import WALKTHROUGHS
from app.providers.registry import CURATED_MODELS, PROVIDER_META, ProviderRegistry

router = APIRouter(prefix="/site", tags=["site"])


async def build_payload() -> dict[str, Any]:
    """Everything the website renders, in one payload."""
    registry = ProviderRegistry()
    providers = []
    for meta in PROVIDER_META:
        providers.append(
            {
                "id": meta.id,
                "label": meta.label,
                "kind": meta.kind,
                "tier": meta.tier,
                "tags": meta.tags,
                "note": meta.note,
                "signup_url": meta.signup_url,
                "requires_key": meta.requires_key,
                "default_base_url": meta.default_base_url,
                "env_key": meta.env_key,
                "has_key": bool(await registry.resolve_key(meta.id)),
            }
        )

    models = [
        {
            "id": m.id,
            "name": m.name,
            "provider": m.provider,
            "provider_label": m.provider_label,
            "description": m.description,
            "context_window": m.context_window,
            "free": m.free,
            "requires_key": m.requires_key,
        }
        for m in CURATED_MODELS
    ]

    return {
        "agents": AGENTS,
        "walkthroughs": WALKTHROUGHS,
        "cheatsheet": CHEATSHEET,
        "cheatsheet_groups": cheatsheet_groups(),
        "loop_stages": LOOP_STAGES,
        "craft": CRAFT,
        "model_guide": MODEL_GUIDE,
        "config_snippets": CONFIG_SNIPPETS,
        "comparison": comparison_matrix(),
        "providers": providers,
        "models": models,
        "harness_layers": HARNESS_LAYERS,
        "harness_projects": HARNESS_PROJECTS,
        "skill_format": SKILL_FORMAT,
        "skill_packages": SKILL_PACKAGES,
        "orchestrators": ORCHESTRATORS,
        "protocols": PROTOCOLS,
        "context_playbook": CONTEXT_PLAYBOOK,
    }


@router.get("")
async def site_content() -> dict[str, Any]:
    return await build_payload()
