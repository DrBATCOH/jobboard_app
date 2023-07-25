from django import forms
from .validators import validate_swear_word


class AddCompanyForm(forms.Form):
    name = forms.CharField(
        label="Company",
        max_length=30,
        strip=True,
        validators=[validate_swear_word]
    )
    employees_number = forms.IntegerField(label="Employees", min_value=1)


class AddVacancyForm(forms.Form):

    LEVELS = (
        ("INTERN", "INTERN"),
        ("JUNIOR", "JUNIOR"),
        ("MIDDLE", "MIDDLE"),
        ("SENIOR", "SENIOR"),
    )

    name = forms.CharField(label="Position", max_length=30, strip=True)
    company = forms.CharField(label="Company", max_length=30, strip=True)
    level = forms.ChoiceField(label="Level", choices=LEVELS)
    expiriens = forms.CharField(label="Expiriens", max_length=10, strip=True)
    min_salary = forms.IntegerField(label="Min Salary", min_value=0, required=False)
    max_salary = forms.IntegerField(label="Max Salary", min_value=0, required=False)
