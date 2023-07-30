from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.business_logic.dto import AddCompanyDTO

from django.db.models import Count
from core.models import Company


def create_company(data: AddCompanyDTO) -> None:
    Company.objects.create(name=data.name, employees_number=data.employees_number)


def get_companies() -> list(Company):
    companies = Company.objects.annotate(vacancy__count=Count("vacancy__id")).order_by("-vacancy__count")
    return list(companies)


def get_company_by_id(company_id: int) -> Company:
    company: Company = Company.objects.annotate(vacancy__count=Count("vacancy__id")).get(pk=company_id)
    return company
