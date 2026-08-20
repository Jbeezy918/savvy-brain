"""GovCon RFI Engine project interface."""

PROJECT_NAME = "GovCon RFI Engine"


def status() -> dict[str, str]:
    return {"name": PROJECT_NAME, "status": "scaffolded"}


def run(**kwargs):
    """Execute the GovCon workflow when parsers are registered."""
    raise NotImplementedError("GovCon execution logic has not been configured yet.")

