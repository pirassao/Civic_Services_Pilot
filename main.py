from civic_services_pilot.staff_assistant import staff_assistant_reply
from civic_services_pilot.tracing import setup_tracing


def main() -> None:
    setup_tracing()
    ticket = "How can I request a copy of a birth certificate?"
    print(f"Answer_staff: {staff_assistant_reply(message=ticket, ticket_id="1", role="staff")}")
    print(f"Answer_customer: {staff_assistant_reply(message=ticket, ticket_id="2", role="customer")}")

if __name__ == "__main__":
    main()