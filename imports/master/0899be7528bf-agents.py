from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import json
import re

from .ha_client import HomeAssistantClient
from .ollama_client import OllamaClient


@dataclass
class ActionProposal:
    agent: str
    summary: str
    domain: str | None = None
    service: str | None = None
    data: dict[str, Any] | None = None
    risk: str = "low"
    requires_approval: bool = False


class SavvyHub:
    def __init__(
        self,
        ha: HomeAssistantClient,
        ollama: OllamaClient,
        model: str,
    ):
        self.ha = ha
        self.ollama = ollama
        self.model = model

    def route(self, request: str) -> str:
        text = request.lower()

        guardian_terms = (
            "unavailable",
            "unknown",
            "low battery",
            "battery",
            "offline",
            "health check",
            "system health",
            "audit",
            "broken device",
            "failed device",
            "check my system",
            "device status",
        )

        if any(term in text for term in guardian_terms):
            return "GUARDIAN"

        builder_terms = (
            "create",
            "build",
            "make",
            "change",
            "turn on",
            "turn off",
            "automation",
            "dashboard",
            "scene",
            "script",
            "integration",
        )

        if any(term in text for term in builder_terms):
            return "BUILDER"

        return "DIRECT"


class Builder:
    def __init__(
        self,
        ha: HomeAssistantClient,
        ollama: OllamaClient,
        model: str,
    ):
        self.ha = ha
        self.ollama = ollama
        self.model = model

    def _extract_first_json_object(self, raw: str) -> dict[str, Any]:
        cleaned = re.sub(r"```(?:json)?", "", raw, flags=re.IGNORECASE)
        cleaned = cleaned.replace("```", "").strip()

        decoder = json.JSONDecoder()

        for index, character in enumerate(cleaned):
            if character != "{":
                continue

            try:
                obj, _ = decoder.raw_decode(cleaned[index:])
            except json.JSONDecodeError:
                continue

            if isinstance(obj, dict):
                return obj

        raise ValueError(f"No valid JSON object found in Builder output: {raw}")

    def propose_service_call(self, request: str) -> ActionProposal:
        services = self.ha.services()

        available = {
            item["domain"]: sorted(item["services"].keys())
            for item in services
            if isinstance(item, dict)
            and "domain" in item
            and isinstance(item.get("services"), dict)
        }

        prompt = (
            "You are a Home Assistant service-call planner.\n"
            "Return exactly one JSON object and nothing else.\n"
            "Do not use services that are not provided.\n"
            "Do not explain your answer.\n\n"
            "Required schema:\n"
            '{"summary":"text","domain":"domain","service":"service",'
            '"data":{},"risk":"low|medium|high"}\n\n'
            "Available services:\n"
            + json.dumps(available)[:14000]
            + "\n\nUser request:\n"
            + request
        )

        raw = self.ollama.generate(self.model, prompt)
        obj = self._extract_first_json_object(raw)

        domain = obj.get("domain")
        service = obj.get("service")

        if domain not in available:
            raise ValueError(f"Builder selected unavailable domain: {domain}")

        if service not in available[domain]:
            raise ValueError(
                f"Builder selected unavailable service: {domain}.{service}"
            )

        risk = str(obj.get("risk", "medium")).lower()

        if risk not in {"low", "medium", "high"}:
            risk = "medium"

        return ActionProposal(
            agent="Builder",
            summary=str(obj.get("summary", request)),
            domain=domain,
            service=service,
            data=obj.get("data") or {},
            risk=risk,
            requires_approval=risk in {"medium", "high"},
        )


class Guardian:
    def __init__(self, ha: HomeAssistantClient):
        self.ha = ha

    def audit(self) -> dict[str, Any]:
        states = self.ha.states()

        unavailable = [
            item["entity_id"]
            for item in states
            if item.get("state") in {"unavailable", "unknown"}
        ]

        low_battery = []

        for item in states:
            attributes = item.get("attributes") or {}

            try:
                value = float(item.get("state"))
            except (TypeError, ValueError):
                continue

            if (
                attributes.get("device_class") == "battery"
                and value <= 20
            ):
                low_battery.append(
                    {
                        "entity_id": item["entity_id"],
                        "percent": value,
                    }
                )

        return {
            "total_entities": len(states),
            "unavailable_count": len(unavailable),
            "unavailable_entities": unavailable[:100],
            "low_battery": low_battery,
        }
