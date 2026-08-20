from http import HTTPStatus
from unittest.mock import patch


class TestSupportFormView:
    def test_view_renders_successfully(self, client):
        response = client.get("/support-form/")
        assert response.status_code == HTTPStatus.OK
        assert "Contact National Data Library" in response.content.decode()

    # TODO: shoudl it be test_support_form_view or test_view ...
    @patch("datagovuk.support.views.ZendeskClient.send_ticket_to_zendesk")
    def test_view_valid_submission(self, mock_zendesk, client):
        form_data = {
            "about": "whole_website",
            "details": "The details of this support request",
            "name": "Test User",
            "email": "test@example.com",
        }
        response = client.post("/support-form/", data=form_data)
        assert response.status_code == HTTPStatus.FOUND
        mock_zendesk.assert_called_once_with(
            [
                "About: whole_website",
                "\nDetails:\nThe details of this support request",
            ],
            "Test User",
            "test@example.com",
        )

    @patch("datagovuk.support.views.ZendeskClient.send_ticket_to_zendesk")
    def test_view_with_page_reference(self, mock_zendesk, client):
        form_data = {
            "about": "specific_page",
            "page_reference": "it is about https://data.gov.uk/test-page/",
            "details": "The details of this support request",
            "name": "Test User",
            "email": "test@example.com",
        }
        response = client.post("/support-form/", data=form_data)
        assert response.status_code == HTTPStatus.FOUND
        mock_zendesk.assert_called_once_with(
            [
                "About: specific_page",
                "Page: it is about https://data.gov.uk/test-page/",
                "\nDetails:\nThe details of this support request",
            ],
            "Test User",
            "test@example.com",
        )

    @patch("datagovuk.support.views.ZendeskClient.send_ticket_to_zendesk")
    def test_view_invalid_submission_missing_page_reference(self, mock_zendesk, client):
        form_data = {
            "about": "specific_page",
            "details": "The details of this support request",
            "name": "Test User",
            "email": "test@example.com",
        }
        response = client.post("/support-form/", data=form_data)
        assert response.status_code == HTTPStatus.OK
        assert "Enter a URL or name of page" in response.content.decode()
