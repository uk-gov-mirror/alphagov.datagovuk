import logging

from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import SupportForm
from .ndl_support_ticket import NDLSupportTicket
from .zendesk import ZendeskClient, ZendeskError

logger = logging.getLogger(__name__)


class SupportFormView(FormView):
    template_name = "support/support_form.jinja"
    form_class = SupportForm
    # TODO: What does success for this page look like
    success_url = reverse_lazy("pages:home")

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        about = cleaned_data["about"]
        page_reference = cleaned_data["page_reference"]
        details = cleaned_data["details"]
        name = cleaned_data["name"] or None
        email = cleaned_data["email"] or None

        message_body = [f"About: {about}"]
        if page_reference:
            message_body.append(f"Page: {page_reference}")
        message_body.append(f"\n{details}")

        ticket = NDLSupportTicket(
            subject="Support request from National Data Library",
            message="\n".join(message_body),
            requester_name=name,
            requester_email=email,
            tags=["national_data_library"],
        )

        zendesk_client = ZendeskClient()
        try:
            zendesk_client.send_ticket_to_zendesk(ticket)
        except ZendeskError:
            logger.exception("Failed to send Zendesk ticket")

        return super().form_valid(form)
