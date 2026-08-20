"""Other Projects interface."""

PROJECT_NAME = "Other Projects"


def status() -> dict[str, str]:
    return {"name": PROJECT_NAME, "status": "ready"}


def run(**kwargs):
    """Dispatch an incubating project after its implementation is registered."""
    raise NotImplementedError("No incubating project execution logic is registered.")

