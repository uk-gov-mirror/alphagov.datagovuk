import logging

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import SupportForm
from .zendesk import ZendeskError, send_ticket_to_zendesk

logger = logging.getLogger(__name__)


class SupportFormView(FormView):
    template_name = "support/support_form.jinja"
    form_class = SupportForm
    success_url = reverse_lazy("support:support-form")

    def form_valid(self, form):
        logger.info(self.request.META)
        cleaned_data = form.cleaned_data

        about = cleaned_data["about"]
        page_reference = cleaned_data["page_reference"]
        details = cleaned_data["details"]
        requester_name = cleaned_data["name"] or None
        requester_email = cleaned_data["email"] or None

        message_body = [f"About: {about}"]
        # TODO: page reference would be the HTTP referer url path + query params?
        if page_reference:
            message_body.append(f"Page: {page_reference}")
        message_body.append(f"\nDetails:\n{details}")

        # TODO: what would the messsage body look like

        try:
            send_ticket_to_zendesk(message_body, requester_name, requester_email)
        except ZendeskError:
            # TODO use the capture_exception util function
            logger.exception("Failed to send Zendesk ticket")
            messages.error(self.request, "Please try again later")
            return self.form_invalid(form)

        messages.success(self.request, "Your support ticket has been successfully sent")
        return super().form_valid(form)
