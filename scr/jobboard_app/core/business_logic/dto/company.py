from dataclasses import dataclass


@dataclass
class AddCompanyDTO:
    name: str
    employees_number: int
