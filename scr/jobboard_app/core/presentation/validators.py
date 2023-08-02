import os
from django.core.exceptions import ValidationError
from core.models import Company
from django.core.files import File


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


def validate_not_exist_company(value: str) -> None:
    if not Company.objects.filter(name=value).exists():
        raise ValidationError(message="Company not exist.")


class ValidateFileExtension:
    def __init__(self, available_extensions: list[str]) -> None:
        self._available_extensions = available_extensions

    def __call__(self, value: File) -> None:
        _, file_extension = os.path.splitext(value.name)
        if not file_extension:
            raise ValidationError(message="File must have an extension")
        if file_extension[1:] not in self._available_extensions:
            raise ValidationError(message=f"Accept only {self._available_extensions}")


class ValidateFileSize:
    def __init__(self, max_size: int) -> None:
        self._max_size = max_size

    def __call__(self, value: File) -> None:
        if value.size > self._max_size:
            max_size = int(self._max_size / 1_000_000)
            raise ValidationError(message=f"Max file size {max_size} MB")
