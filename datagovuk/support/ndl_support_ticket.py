import dataclasses


@dataclasses.dataclass
class NDLSupportTicket:
    subject: str
    message: str
    requester_name: str | None = None
    requester_email: str | None = None
    tags: list[str] = dataclasses.field(default_factory=list)

    @property
    def request_data(self):
        data = {
            "ticket": {
                "subject": self.subject,
                "comment": {"body": self.message, "public": False},
                "tags": self.tags,
            },
        }

        if self.requester_email:
            data["ticket"]["requester"] = {
                "email": self.requester_email,
                "name": self.requester_name or self.requester_email,
            }

        return data
