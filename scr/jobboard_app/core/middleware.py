from __future__ import annotations
from django.http import HttpResponseBadRequest
from typing import Callable, TYPE_CHECKING


if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


class BlockURLMiddleware:
    BLOCK_URLS = ("/block",)

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.path in self.BLOCK_URLS:
            return HttpResponseBadRequest(content="This url blocked.")
        response = self.get_response(request)
        return response