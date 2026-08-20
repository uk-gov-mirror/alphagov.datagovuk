from django import forms
from django.db import models


class SupportForm(forms.Form):
    class AboutChoices(models.TextChoices):
        WHOLE_WEBSITE = "whole_website", "The whole website"
        SPECIFIC_PAGE = "specific_page", "A specific page"

    about = forms.ChoiceField(
        label="What's it to do with?",
        choices=AboutChoices.choices,
        widget=forms.RadioSelect,
    )
    page_reference = forms.CharField(
        required=False,
        label="Enter URL or name of page",
    )
    details = forms.CharField(
        widget=forms.Textarea,
        label="What are the details",
    )
    name = forms.CharField(
        required=False,
        label="Your name",
    )
    email = forms.EmailField(
        required=False,
        label="Your email address",
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("about") == self.AboutChoices.SPECIFIC_PAGE.value and not cleaned_data.get(
            "page_reference",
        ):
            self.add_error("page_reference", "Enter a URL or name of page")
        return cleaned_data
