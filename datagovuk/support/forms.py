from django import forms


class SupportForm(forms.Form):
    about = forms.ChoiceField(
        label="What's it to do with?",
        choices=[
            ("whole_website", "The whole website"),
            ("specific_page", "A specific page"),
        ],
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
        if cleaned_data["about"] == "specific_page" and not cleaned_data["page_reference"]:
            self.add_error("page_reference", "Enter a URL or name of page")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["about"].widget.attrs.update({"class": "govuk-radios__input"})
