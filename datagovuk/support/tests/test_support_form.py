from datagovuk.support.forms import SupportForm


class TestSupportForm:
    def test_valid_form_submission(self):
        form = SupportForm(
            data={
                "about": "whole_website",
                "details": "about /test page",
                "name": "Test User",
                "email": "test@example.com",
            },
        )
        assert form.is_valid()
        assert form.cleaned_data["about"] == "whole_website"
        assert form.cleaned_data["details"] == "about /test page"
        assert form.cleaned_data["name"] == "Test User"
        assert form.cleaned_data["email"] == "test@example.com"

    def test_invalid_form_submission(self):
        form = SupportForm(
            data={
                "about": "specific_page",
                "details": "This is a test support request.",
                "name": "Test User",
                "email": "test@example.com",
            },
        )
        assert not form.is_valid()
        assert "page_reference" in form.errors

    def test_page_reference_provided_with_specific_page(self):
        form = SupportForm(
            data={
                "about": "specific_page",
                "page_reference": "https://test.com",
                "details": "This is a test support request.",
                "name": "Test User",
                "email": "test@example.com",
            },
        )
        assert form.is_valid()
        assert form.cleaned_data["about"] == "specific_page"
        assert form.cleaned_data["page_reference"] == "https://test.com"

    def test_non_required_fields_allowed_with_form_submission(self):
        form = SupportForm(
            data={
                "about": "whole_website",
                "details": "General support request",
                "name": "",
                "email": "",
            },
        )
        assert form.is_valid()
        assert form.cleaned_data["name"] == ""
        assert form.cleaned_data["email"] == ""
        assert form.cleaned_data["details"] == "General support request"

    def test_details_has_more_than_max_length(self):
        max_length = 1200
        details = "*" * (max_length + 1)

        form = SupportForm(
            data={
                "about": "whole_website",
                "details": details,
                "name": "Test User",
                "email": "test@example.com",
            },
        )
        assert not form.is_valid()
        assert "details" in form.errors
