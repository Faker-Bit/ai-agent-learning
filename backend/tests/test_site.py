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
