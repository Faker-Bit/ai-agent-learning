from __future__ import annotations

import httpx
import pytest

from app.content.agents import AGENTS, AGENT_IDS
from app.content.cheatsheet import CHEATSHEET
from app.content.guide import CRAFT, LOOP_STAGES, MODEL_GUIDE
from app.content.walkthroughs import WALKTHROUGHS


async def test_health(client: httpx.AsyncClient) -> None:
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["service"] == "agent-pilot-backend"


async def test_site_payload(client: httpx.AsyncClient) -> None:
    resp = await client.get("/api/site")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["agents"]) == len(AGENTS) >= 12
    assert len(body["walkthroughs"]) == len(WALKTHROUGHS) >= 8
    assert len(body["cheatsheet"]) == len(CHEATSHEET) >= 60
    assert body["loop_stages"]
    assert body["craft"]
    assert body["model_guide"]
    assert body["config_snippets"]
    assert body["comparison"]
    assert body["providers"]
    assert body["models"]


def test_agent_catalog_integrity() -> None:
    assert len(AGENT_IDS) == len(set(AGENT_IDS)), "duplicate agent id"
    for agent in AGENTS:
        assert agent["name"]
        assert agent["tagline"]
        assert agent["kind"]
        assert agent["install"], f"{agent['id']} has no install command"
        assert agent["best_for"]
        assert len(agent["highlights"]) >= 4
        # A command list is only required when the commands were verified
        # against the tool's own documentation.
        if agent.get("verified", True):
            assert agent["commands"], f"{agent['id']} has no command list"
        for command, description in agent["commands"]:
            assert command and description
        if agent.get("stars"):
            assert agent["stars"].endswith("k") or agent["stars"].isdigit()


def test_walkthrough_integrity() -> None:
    agent_ids = set(AGENT_IDS)
    seen: set[str] = set()
    for walkthrough in WALKTHROUGHS:
        assert walkthrough["id"] not in seen
        seen.add(walkthrough["id"])
        assert walkthrough["agent"] in agent_ids
        assert walkthrough["title"]
        assert walkthrough["summary"]
        assert walkthrough["outcome"]
        assert len(walkthrough["steps"]) >= 5, f"{walkthrough['id']} is too short"
        for step in walkthrough["steps"]:
            assert step["title"]
            assert step["narration"], f"{walkthrough['id']}/{step['id']} has no narration"
            assert step["lines"], f"{walkthrough['id']}/{step['id']} has no terminal lines"
            for line in step["lines"]:
                assert line["type"] in {
                    "input", "output", "tool", "success", "info", "warn", "muted",
                    "accent", "diff",
                }, f"unknown line type {line['type']}"
                assert line["text"]


def test_agent_walkthrough_links_resolve() -> None:
    walkthrough_ids = {w["id"] for w in WALKTHROUGHS}
    for agent in AGENTS:
        for ref in agent["walkthroughs"]:
            assert ref in walkthrough_ids, f"{agent['id']} points at missing {ref}"


def test_cheatsheet_integrity() -> None:
    agent_ids = set(AGENT_IDS)
    for row in CHEATSHEET:
        assert row["agent"] in agent_ids, f"unknown agent in cheatsheet: {row['agent']}"
        assert row["command"]
        assert row["description"]
        assert row["group"]


def test_guide_integrity() -> None:
    for stage in LOOP_STAGES:
        assert stage["title"] and stage["body"] and stage["you_control"]
    for craft in CRAFT:
        assert craft["title"] and craft["body"] and craft["rule"]
        assert craft["before"]["lines"] and craft["after"]["lines"]
    for guide in MODEL_GUIDE:
        assert guide["title"] and guide["rows"]


def test_harness_content_integrity() -> None:
    from app.content.harness import (
        CONTEXT_PLAYBOOK,
        HARNESS_LAYERS,
        HARNESS_PROJECTS,
        ORCHESTRATORS,
        PROTOCOLS,
        SKILL_FORMAT,
        SKILL_PACKAGES,
    )

    assert len(HARNESS_LAYERS) == 7
    for layer in HARNESS_LAYERS:
        assert layer["title"] and layer["body"] and layer["control"] and layer["fails"]

    assert len(HARNESS_PROJECTS) >= 6
    for project in HARNESS_PROJECTS:
        assert project["name"] and project["repo"].count("/") == 1
        assert project["why"] and project["steal"]

    assert SKILL_FORMAT["example"].startswith("---")
    assert "SKILL.md" in " ".join(SKILL_FORMAT["locations"])
    assert SKILL_FORMAT["frontmatter"]

    assert len(SKILL_PACKAGES) >= 8
    for package in SKILL_PACKAGES:
        assert package["name"] and package["repo"] and package["what"]

    assert len(ORCHESTRATORS) >= 6
    for orchestrator in ORCHESTRATORS:
        assert orchestrator["name"] and orchestrator["repo"] and orchestrator["what"]

    assert len(PROTOCOLS) >= 5
    for protocol in PROTOCOLS:
        assert protocol["name"] and protocol["what"] and protocol["example"]

    assert len(CONTEXT_PLAYBOOK) >= 4
    for entry in CONTEXT_PLAYBOOK:
        assert entry["title"] and entry["body"] and entry["bad"] and entry["good"]


def test_walkthrough_covers_skills() -> None:
    ids = {w["id"] for w in WALKTHROUGHS}
    assert "opencode-skills" in ids
    skills = next(w for w in WALKTHROUGHS if w["id"] == "opencode-skills")
    assert any("SKILL.md" in line["text"] for step in skills["steps"] for line in step["lines"])


def test_model_hub_integrity() -> None:
    from app.content.models_hub import HUB_INTRO, MODEL_HUB

    assert len(MODEL_HUB) >= 10
    vendors = {model["vendor"] for model in MODEL_HUB}
    assert {"OpenAI", "Anthropic", "Google", "DeepSeek", "xAI", "Alibaba"} <= vendors
    for model in MODEL_HUB:
        assert model["name"] and model["vendor"] and model["blurb"]
        assert model["tier"] in ("free", "paid", "local", "free+paid")
        assert len(model["best_for"]) >= 3
        assert len(model["surfaces"]) >= 2
        assert len(model["prompting"]) >= 4
        assert len(model["agent_notes"]) >= 1
        assert len(model["limits"]) >= 1
        assert model["api"]["base_url"].startswith("http")
        assert model["api"]["code"].strip()
        assert model["api"]["env"]
        assert len(model["links"]) >= 2
    assert HUB_INTRO["body"]
    assert len(HUB_INTRO["principles"]) >= 4


def test_security_lab_integrity() -> None:
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

    assert len(ATTACK_TAXONOMY) >= 8
    for entry in ATTACK_TAXONOMY:
        assert entry["name"] and entry["owasp"] and entry["atlas"]
        assert entry["mechanism"] and entry["detect"] and entry["defend"]
        # the lab teaches structure, not turnkey payloads
        assert "sanitised" in entry["example"].lower() or "structure" in entry["example"].lower()

    assert len(DETECTION_SIGNATURES) >= 5
    for signature in DETECTION_SIGNATURES:
        assert signature["name"] and signature["pattern"] and signature["channel"]

    assert len(DEFENCE_LAYERS) >= 6
    for layer in DEFENCE_LAYERS:
        assert layer["title"] and layer["how"] and layer["limits"]

    assert len(TEST_PLAYBOOK) >= 6
    for step in TEST_PLAYBOOK:
        assert step["title"] and step["body"]

    assert len(RESEARCH_FINDINGS) >= 3
    for finding in RESEARCH_FINDINGS:
        assert finding["title"] and finding["link"].startswith("http")
        assert finding["rows"] and finding["lesson"]

    assert len(FRAMEWORKS) >= 4
    assert len(WHERE_TO_LOOK) >= 5
    assert len(PROMPT_LAB_PLAYBOOK) >= 5


def test_resources_catalogue_integrity() -> None:
    from app.content.resources import GENERATED, RESOURCE_CATEGORIES, RESOURCES

    assert len(RESOURCES) >= 60
    assert len(RESOURCE_CATEGORIES) >= 8
    category_ids = {category["id"] for category in RESOURCE_CATEGORIES}
    for item in RESOURCES:
        assert item["repo"].count("/") == 1
        assert item["url"].startswith("https://github.com/")
        assert item["category"] in category_ids
        assert item["description"]
        assert item["stars"] >= 0
        assert item["license"]
        assert item["note"], f"{item['repo']} has no usage note"
    ids = [item["id"] for item in RESOURCES]
    assert len(ids) == len(set(ids)), "duplicate resource id"
    assert GENERATED


async def test_resources_endpoint(client: httpx.AsyncClient) -> None:
    resp = await client.get("/api/site/resources")
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] >= 60
    assert body["matched"] == body["total"]
    assert body["categories"]

    filtered = await client.get("/api/site/resources", params={"category": "prompt-security"})
    assert filtered.status_code == 200
    assert filtered.json()["matched"] > 0
    assert all(r["category"] == "prompt-security" for r in filtered.json()["resources"])

    searched = await client.get("/api/site/resources", params={"q": "garak"})
    assert searched.status_code == 200
    assert searched.json()["matched"] >= 1
