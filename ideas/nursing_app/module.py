"""Nursing App project interface."""

PROJECT_NAME = "Nursing App"


def status() -> dict[str, str]:
    return {"name": PROJECT_NAME, "status": "scaffolded"}


def run(**kwargs):
    """Execute Nursing App logic when an implementation is registered."""
    raise NotImplementedError("Nursing App execution logic has not been configured yet.")

