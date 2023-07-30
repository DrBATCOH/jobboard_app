from django import forms

from core.presentation.validators import validate_swear_word
from core.models import Level, Expirience


class AddCompanyForm(forms.Form):
    name = forms.CharField(
        label="Company", max_length=30, strip=True, validators=[validate_swear_word]
    )
    employees_number = forms.IntegerField(label="Employees", min_value=1)
