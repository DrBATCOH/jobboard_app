from django.core.exceptions import ValidationError


def validate_swear_word(value: str) -> None:
    if "fuck" in value.lower():
        raise ValidationError(message="swear word")
    return None
