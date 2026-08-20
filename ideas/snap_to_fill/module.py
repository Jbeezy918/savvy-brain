"""SnapToFill project interface."""

PROJECT_NAME = "SnapToFill"


def status() -> dict[str, str]:
    return {"name": PROJECT_NAME, "status": "scaffolded"}


def run(**kwargs):
    """Execute SnapToFill logic when an implementation is registered."""
    raise NotImplementedError("SnapToFill execution logic has not been configured yet.")

