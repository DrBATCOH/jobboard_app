from django import forms

from core.presentation.validators import (
    ValidateMaxTags,
    validate_not_exist_company,
    ValidateFileExtension,
    ValidateFileSize
)
from core.models import Level, Expirience

LEVELS = [(level.name, level.name) for level in Level.objects.all()]

EXPIRIENCE = [(expirience.name, expirience.name) for expirience in Expirience.objects.all()]


class AddVacancyForm(forms.Form):

    name = forms.CharField(label="Position", max_length=30, strip=True)
    company = forms.CharField(label="Company", max_length=30, strip=True, validators=[validate_not_exist_company])
    level_name = forms.ChoiceField(label="Level", choices=LEVELS)
    expirience = forms.ChoiceField(label="Expiriens", choices=EXPIRIENCE)
    min_salary = forms.IntegerField(label="Min Salary", min_value=0, required=False)
    max_salary = forms.IntegerField(label="Max Salary", min_value=0, required=False)
    attachment = forms.FileField(label="Attachment", allow_empty_file=False, validators=[ValidateFileExtension("pdf"), ValidateFileSize(max_size=5_000_000)])
    tags = forms.CharField(label="Tags", widget=forms.Textarea, validators=[ValidateMaxTags(max_count=5)], required=False)


class SearchVacancyForm(forms.Form):
    template_name = "search_form_snippet.html"

    position = forms.CharField(label="Position", max_length=30, strip=True, required=False)
    company = forms.CharField(label="Company", max_length=30, strip=True, required=False)
    level_name = forms.ChoiceField(label="Level", choices=[("", "ALL")] + LEVELS, required=False)
    expirience = forms.ChoiceField(label="Expiriens", choices=[("", "ALL")] + EXPIRIENCE, required=False)
    min_salary = forms.IntegerField(label="Min Salary", min_value=0, required=False)
    max_salary = forms.IntegerField(label="Max Salary", min_value=0, required=False)
    tag = forms.CharField(label="Tag", required=False)
