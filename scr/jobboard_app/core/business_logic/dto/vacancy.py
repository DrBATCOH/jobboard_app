from dataclasses import dataclass

from django.core.files import File


@dataclass
class SearchVacancyDTO:
    position: str
    company: str
    level_name: str
    expirience: str
    min_salary: int | None
    max_salary: int | None
    tag: str


@dataclass
class AddVacancyDTO:
    name: str
    company: str
    level_name: str
    expirience: str
    min_salary: int | None
    max_salary: int | None
    attachment: File
    tags: str
