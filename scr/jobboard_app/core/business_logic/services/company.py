from __future__ import annotations

from typing import TYPE_CHECKING


from django.db.models import Count


if TYPE_CHECKING:
    from core.business_logic.dto import AddCompanyDTO

from core.models import Company
from core.business_logic.services.common import replece_file_name_to_uupd, optimize_image


def create_company(data: AddCompanyDTO) -> None:
    data.logo = replece_file_name_to_uupd(file=data.logo)
    data.logo = optimize_image(file=data.logo)
    Company.objects.create(name=data.name, employees_number=data.employees_number, logo=data.logo)


def get_companies() -> list(Company):
    companies = Company.objects.annotate(vacancy__count=Count("vacancy__id")).order_by("-vacancy__count")
    return list(companies)


def get_company_by_id(company_id: int) -> Company:
    company: Company = Company.objects.annotate(vacancy__count=Count("vacancy__id")).get(pk=company_id)
    return company
