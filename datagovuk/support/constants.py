from django.db import models


class AboutChoices(models.TextChoices):
    WHOLE_WEBSITE = "whole_website", "The whole website"
    SPECIFIC_PAGE = "specific_page", "A specific page"
