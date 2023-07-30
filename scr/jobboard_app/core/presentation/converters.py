from dacite import from_dict
from typing import Any, TypeVar


T = TypeVar("T")

def convert_data_from_form_to_dto(dto: type[T], data_from_form: dict[str, Any]) -> T:
    return from_dict(dto, data_from_form)