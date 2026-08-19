import logging
from http import HTTPStatus

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class ZendeskClient:
    """
    A ZendeskClient copied from the alphagov/notifications-utils repo
    """

    # the account used to authenticate with. If no requester is provided, the ticket will come from this account.
    NOTIFY_ZENDESK_EMAIL = "... NDL email"

    ZENDESK_TICKET_URL = "https://govuk.zendesk.com/api/v2/tickets.json"

    def __init__(self):
        self.api_key = settings.ZENDESK_API_KEY
        self.requests_session = requests.Session()

    def send_ticket_to_zendesk(self, ticket):
        response = self.requests_session.post(
            self.ZENDESK_TICKET_URL,
            json=ticket.request_data,
            auth=(f"{self.NOTIFY_ZENDESK_EMAIL}/token", self.api_key),
            headers={"Content-type": "application/json"},
        )

        if response.status_code != HTTPStatus.CREATED:
            if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY and self._is_user_suspended(response.json()):
                error_message = response.json()["details"]
                logger.warning("Zendesk create ticket failed because user is suspended: %r", error_message)
                return None
            logger.error(
                "Zendesk create ticket request failed with %s: %r",
                response.status_code,
                response.json(),
                extra={"status_code": response.status_code},
            )
            raise ZendeskError(response)

        ticket_id = response.json()["ticket"]["id"]

        logger.info(
            "Zendesk create ticket %s succeeded",
            ticket_id,
            extra={"zendesk_ticket_id": ticket_id, "zendesk_operation": "create"},
        )

        return ticket_id

    def _is_user_suspended(self, response):
        requester_error = response["details"].get("requester")
        return requester_error and ("suspended" in requester_error[0]["description"])


class ZendeskError(Exception):
    def __init__(self, response):
        self.response = response
