from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import json

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
    def __init__(self, ha: HomeAssistantClient, ollama: OllamaClient, model: str):
        self.ha = ha
        self.ollama = ollama
        self.model = model

    def route(self, request: str) -> str:
        prompt = (
            "Classify this Home Assistant request as BUILDER, GUARDIAN, or DIRECT. "
            "Return only one label. Request: " + request
        )
        label = self.ollama.generate(self.model, prompt).upper()
        if "GUARDIAN" in label:
            return "GUARDIAN"
        if "BUILDER" in label:
            return "BUILDER"
        return "DIRECT"

class Builder:
    def __init__(self, ha: HomeAssistantClient, ollama: OllamaClient, model: str):
        self.ha = ha
        self.ollama = ollama
        self.model = model

    def propose_service_call(self, request: str) -> ActionProposal:
        services = self.ha.services()
        available = {
            item["domain"]: sorted(item["services"].keys())
            for item in services
            if isinstance(item, dict) and "domain" in item and "services" in item
        }

        prompt = (
            "You are a Home Assistant service-call planner. "
            "Use only services in this JSON: "
            + json.dumps(available)[:12000]
            + '\nReturn strict JSON with keys summary, domain, service, data, risk. '
            + "Risk must be low, medium, or high. Request: "
            + request
        )

        raw = self.ollama.generate(self.model, prompt)
        try:
            start, end = raw.index("{"), raw.rindex("}") + 1
            obj = json.loads(raw[start:end])
        except Exception as exc:
            raise ValueError(f"Builder returned invalid JSON: {raw}") from exc

        domain = obj.get("domain")
        service = obj.get("service")
        if domain not in available or service not in available[domain]:
            raise ValueError(f"Builder selected unavailable service: {domain}.{service}")

        risk = obj.get("risk", "medium")
        return ActionProposal(
            agent="Builder",
            summary=obj.get("summary", request),
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
            item["entity_id"] for item in states
            if item.get("state") in {"unavailable", "unknown"}
        ]

        low_battery = []
        for item in states:
            attrs = item.get("attributes") or {}
            try:
                value = float(item.get("state"))
            except (TypeError, ValueError):
                continue
            if attrs.get("device_class") == "battery" and value <= 20:
                low_battery.append({"entity_id": item["entity_id"], "percent": value})

        return {
            "total_entities": len(states),
            "unavailable_count": len(unavailable),
            "unavailable_entities": unavailable[:100],
            "low_battery": low_battery,
        }
