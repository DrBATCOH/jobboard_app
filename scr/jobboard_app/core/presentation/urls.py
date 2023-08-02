from django.urls import path

from core.presentation.views import (
    index,
    add_company,
    company_list,
    add_vacancy,
    get_vacancy,
    get_company
)

urlpatterns = [
    path("", index, name="index"),
    path("company/add/", add_company, name="company_add"),
    path("company/", company_list, name="company_list"),
    path("vacancy/add/", add_vacancy, name="vacancy_add"),
    path("vacancy/<int:vacancy_id>/", get_vacancy, name="vacancy"),
    path("company/<int:company_id>/", get_company, name="company"),
]

