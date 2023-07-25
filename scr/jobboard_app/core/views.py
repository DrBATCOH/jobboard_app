from __future__ import annotations
import timeit
from django.http import (HttpResponse,
                         HttpResponseRedirect,
                         HttpResponseBadRequest
                         )
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest

from .services import (CompanyStorage,
                       VacancyStorage,
                       Vacancy,
                       Company
                       )

from .forms import (AddCompanyForm,
                    AddVacancyForm,
                    )


company_storage = CompanyStorage()
vacancy_storage = VacancyStorage(company_storage=company_storage)


@require_http_methods(request_method_list=["GET"])
def index(request: HttpRequest) -> HttpResponse:
    vacancies = vacancy_storage.get_all_vacanies()
    context = {"vacancies": vacancies}
    return render(request=request, template_name="index.html", context=context)


@require_http_methods(request_method_list=["GET", "POST"])
def add_company(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = AddCompanyForm()
        context = {"form": form}
        return render(request=request, template_name="company_add.html", context=context)

    elif request.method == "POST":
        form = AddCompanyForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            employees_number = form.cleaned_data["employees_number"]
            company = Company(
                name=name,
                employees_number=employees_number
            )
            company_storage.add_company(company_to_add=company)
        else:
            return HttpResponseBadRequest(content="Form validation failed.")
    return HttpResponseRedirect(redirect_to=reverse("company_list"))


@require_http_methods(request_method_list=["GET"])
def company_list(request: HttpRequest) -> HttpResponse:
    companies = company_storage.get_all_companies()
    context = {"companies": companies}
    return render(request=request, template_name="company_list.html", context=context)


@require_http_methods(request_method_list=["GET", "POST"])
def add_vacancy(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = AddVacancyForm()
        context = {"form": form}
        return render(request=request, template_name="vacancy_add.html", context=context)

    elif request.method == "POST":
        form = AddVacancyForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            company = form.cleaned_data["company"]
            level = form.cleaned_data["level"]
            expiriens = form.cleaned_data["expiriens"]
            min_salary = form.cleaned_data["min_salary"]
            max_salary = form.cleaned_data["max_salary"]

            vacancy = Vacancy(
                name=name,
                company=company,
                level=level,
                expiriens=expiriens,
                min_salary=min_salary,
                max_salary=max_salary
            )
            vacancy_storage.add_vacancy(vacancy_to_add=vacancy)
        else:
            return HttpResponseBadRequest(content="Form validation failed.")
        return HttpResponseRedirect(redirect_to=reverse("index"))


@require_http_methods(request_method_list=["GET"])
def get_vacancy(request: HttpRequest, vacancy_id: int) -> HttpResponse:
    vacancy = vacancy_storage.get_vacancy_id(vacancy_id=vacancy_id)
    context = {"vacancy": vacancy}
    return render(request=request, template_name="get_vacancy.html", context=context)


@require_http_methods(request_method_list=["GET"])
def get_company(request: HttpRequest, company_id: int) -> HttpResponse:
    company = company_storage.get_company_id(company_id=company_id)
    context = {"company": company}
    return render(request=request, template_name="get_company.html", context=context)
