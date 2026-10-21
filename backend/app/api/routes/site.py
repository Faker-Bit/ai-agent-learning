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
from app.content.models_hub import HUB_INTRO, MODEL_HUB
from app.content.resources import GENERATED, RESOURCE_CATEGORIES, RESOURCES
from app.content.security_lab import (
    ATTACK_TAXONOMY,
    DEFENCE_LAYERS,
    DETECTION_SIGNATURES,
    FRAMEWORKS,
    PROMPT_LAB_PLAYBOOK,
    RESEARCH_FINDINGS,
    TEST_PLAYBOOK,
    WHERE_TO_LOOK,
)
from app.content.walkthroughs import WALKTHROUGHS
from app.providers.registry import CURATED_MODELS, PROVIDER_META, ProviderRegistry

router = APIRouter(prefix="/site", tags=["site"])
# Short alias so the catalogue is also reachable at /api/resources.
resources_router = APIRouter(prefix="/resources", tags=["resources"])


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
        "model_hub": MODEL_HUB,
        "hub_intro": HUB_INTRO,
        "security_lab": {
            "taxonomy": ATTACK_TAXONOMY,
            "signatures": DETECTION_SIGNATURES,
            "defences": DEFENCE_LAYERS,
            "playbook": TEST_PLAYBOOK,
            "findings": RESEARCH_FINDINGS,
            "frameworks": FRAMEWORKS,
            "where_to_look": WHERE_TO_LOOK,
            "lab": PROMPT_LAB_PLAYBOOK,
        },
    }


@router.get("/resources")
@resources_router.get("")
async def resources(
    q: str = "", category: str = "", limit: int = 200
) -> dict[str, Any]:
    """The GitHub research catalogue, filtered. Kept out of /site so the page stays fast."""
    needle = q.strip().lower()
    picked: list[dict[str, Any]] = []
    for item in RESOURCES:
        if category and item["category"] != category:
            continue
        if needle:
            haystack = " ".join(
                [
                    item["name"],
                    item["repo"],
                    item.get("description", ""),
                    item.get("note", ""),
                    " ".join(item.get("topics", [])),
                ]
            ).lower()
            if needle not in haystack:
                continue
        picked.append(item)
        if len(picked) >= limit:
            break

    return {
        "generated": GENERATED,
        "categories": RESOURCE_CATEGORIES,
        "resources": picked,
        "total": len(RESOURCES),
        "matched": len(picked),
    }


@router.get("")
async def site_content() -> dict[str, Any]:
    return await build_payload()
