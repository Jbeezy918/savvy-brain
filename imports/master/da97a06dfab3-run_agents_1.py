import json
from savvy_ha.config import Settings
from savvy_ha.ha_client import HomeAssistantClient
from savvy_ha.ollama_client import OllamaClient
from savvy_ha.agents import SavvyHub, Builder, Guardian

def main():
    settings = Settings()
    settings.validate()

    ha = HomeAssistantClient(settings.ha_url, settings.ha_token)
    ollama = OllamaClient(settings.ollama_url)

    hub = SavvyHub(ha, ollama, settings.ollama_model)
    builder = Builder(ha, ollama, settings.builder_model)
    guardian = Guardian(ha)

    print("Savvy HA Agents ready. Type 'quit' to exit.")
    while True:
        request = input("\nJoe> ").strip()
        if not request:
            continue
        if request.lower() in {"quit", "exit"}:
            break

        route = hub.route(request)
        if route == "GUARDIAN":
            print(json.dumps(guardian.audit(), indent=2))
            continue

        proposal = builder.propose_service_call(request)
        print(json.dumps(proposal.__dict__, indent=2))

        if settings.dry_run:
            print("DRY_RUN=true: no Home Assistant action was executed.")
            continue

        if proposal.requires_approval:
            approved = input("Approve this action? Type YES: ").strip() == "YES"
            if not approved:
                print("Cancelled.")
                continue

        result = ha.call_service(
            proposal.domain,
            proposal.service,
            proposal.data or {},
        )
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
