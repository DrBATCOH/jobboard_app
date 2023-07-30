from typing import Any
from django.core.exceptions import ValidationError
from core.models import Company


def validate_swear_word(value: str) -> None:
    if "fuck" in value.lower():
        raise ValidationError(message="swear word")
    return None


class ValidateMaxTags:
    def __init__(self, max_count: int) -> None:
        self._max_count = max_count

    def __call__(self, value: str) -> None:
        number_of_tags = len(value.split("\r\n"))

        if number_of_tags > self._max_count:
            raise ValidationError(message=f"Max number of tags is {self._max_count}")
        else:
            return None


def validate_not_exist_company(value:str) -> None:
    if not Company.objects.filter(name=value).exists():
        raise ValidationError(message="Company not exist.")