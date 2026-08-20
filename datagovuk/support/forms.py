from django import forms

from .constants import AboutChoices


class SupportForm(forms.Form):
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
        max_length=1200,
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
        if cleaned_data.get("about") == AboutChoices.SPECIFIC_PAGE.value and not cleaned_data.get("page_reference"):
            self.add_error("page_reference", "Enter a URL or name of page")
        return cleaned_data
