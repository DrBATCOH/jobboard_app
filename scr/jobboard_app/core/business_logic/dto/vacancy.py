from dataclasses import dataclass


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
    tags: str
