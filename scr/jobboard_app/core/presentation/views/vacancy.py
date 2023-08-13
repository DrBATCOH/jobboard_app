from __future__ import annotations
from typing import TYPE_CHECKING

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods


if TYPE_CHECKING:
    from django.http import HttpRequest

from core.presentation.forms import SearchVacancyForm, AddVacancyForm
from core.business_logic.services import search_vacancies, create_vacancy, get_vacancy_by_id
from core.business_logic.errors import CompanyNotExists
from core.business_logic.dto import SearchVacancyDTO, AddVacancyDTO
from core.presentation.converters import convert_data_from_form_to_dto


@require_http_methods(request_method_list=["GET"])
def index(request: HttpRequest) -> HttpResponse:
    filters_form = SearchVacancyForm(request.GET)
    if filters_form.is_valid():
        search_filters = convert_data_from_form_to_dto(SearchVacancyDTO, filters_form.cleaned_data)
        vacancies = search_vacancies(search_filters=search_filters)
        form = SearchVacancyForm()
        context = {"vacancies": vacancies, "form": form}
        return render(request=request, template_name="index.html", context=context)
    else:
        context = {"vacancies": vacancies, "form": form}
        return render(request=request, template_name="index.html", context=context)


@require_http_methods(request_method_list=["GET", "POST"])
def add_vacancy(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = AddVacancyForm()
        context = {"form": form}
        return render(
            request=request, template_name="vacancy_add.html", context=context
        )

    elif request.method == "POST":
        form = AddVacancyForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            data = convert_data_from_form_to_dto(AddVacancyDTO, form.cleaned_data)
            try:
                create_vacancy(data=data)
            except CompanyNotExists:
                context = {"form": form}
                return render(request=request, template_name="vacancy_add.html", context=context)
        else:
            context = {"form": form}
            return render(request=request, template_name="vacancy_add.html", context=context)
        return HttpResponseRedirect(redirect_to=reverse("index"))


@require_http_methods(request_method_list=["GET"])
def get_vacancy(request: HttpRequest, vacancy_id: int) -> HttpResponse:
    vacancy, tags = get_vacancy_by_id(vacancy_id=vacancy_id)
    context = {"vacancy": vacancy, "tags": tags}
    return render(request=request, template_name="get_vacancy.html", context=context)
