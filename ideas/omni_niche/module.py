"""Omni-Niche Synthesis Engine project interface."""

PROJECT_NAME = "Omni-Niche Synthesis Engine"


def status() -> dict[str, str]:
    return {"name": PROJECT_NAME, "status": "scaffolded"}


def run(**kwargs):
    """Execute synthesis logic when a pipeline is registered."""
    raise NotImplementedError("Omni-Niche execution logic has not been configured yet.")

