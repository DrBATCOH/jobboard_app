from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.business_logic.dto import SearchVacancyDTO, AddVacancyDTO

from django.db import transaction

from core.models import Vacancy, Company, Tag, Level, Expirience
from core.business_logic.errors import CompanyNotExists
from core.business_logic.services.common import replece_file_name_to_uupd


def search_vacancies(search_filters: SearchVacancyDTO) -> list[Vacancy]:
    vacancies = Vacancy.objects.select_related("level", "company").prefetch_related("tags")

    if search_filters.position:
        vacancies = vacancies.filter(name__icontains=search_filters.position)

    if search_filters.company:
        vacancies = vacancies.filter(company__name__icontains=search_filters.company)

    if search_filters.level_name:
        vacancies = vacancies.filter(level__name=search_filters.level_name)

    if search_filters.expirience:
        vacancies = vacancies.filter(expirience__name=search_filters.expirience)

    if search_filters.min_salary:
        vacancies = vacancies.filter(min_salary__gte=search_filters.min_salary)

    if search_filters.max_salary:
        vacancies = vacancies.filter(max_salary__lte=search_filters.max_salary)

    if search_filters.tag:
        vacancies = vacancies.filter(tags__name=search_filters.tag)
    
    vacancies = vacancies.order_by("-id")

    return list(vacancies)


def create_vacancy(data: AddVacancyDTO) -> None:
    with transaction.atomic():
        tags: list[str] = data.tags.split("\r\n")
        tags_list: list[Tag] = []
        for tag in tags:
            tag = tag.lower()
            try:
                tags_from_db = Tag.objects.get(name=tag)
            except Tag.DoesNotExist:
                tags_from_db = Tag.objects.create(name=tag)
            tags_list.append(tags_from_db)

        level = Level.objects.get(name=data.level_name)
        expirience = Expirience.objects.get(name=data.expirience)
        try:
            company = Company.objects.get(name=data.company)
        except Company.DoesNotExist:
            raise CompanyNotExists

        data.attachment = replece_file_name_to_uupd(file=data.attachment)
        
        created_vacancy = Vacancy.objects.create(
            name=data.name,
            company=company,
            level=level,
            expirience=expirience,
            min_salary=data.min_salary,
            max_salary=data.max_salary,
            attachment=data.attachment
        )

        created_vacancy.tags.set(tags_list)


def get_vacancy_by_id(vacancy_id: int) -> tuple[Vacancy, list[Tag]]:
    vacancy: Vacancy = Vacancy.objects.select_related("level", "company").prefetch_related("tags").get(pk=vacancy_id)
    tags = vacancy.tags.all()
    return vacancy, list(tags)
