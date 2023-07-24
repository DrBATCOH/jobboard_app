from __future__ import annotations
from django.http import (HttpResponse,
                         HttpResponseRedirect
                         )
from django.shortcuts import render

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest

from .services import (CompanyStorage,
                       VacancyStorage,
                       Vacancy,
                       Company
                       )


company_storage = CompanyStorage()
vacancy_storage = VacancyStorage(company_storage=company_storage)


def index(request: HttpRequest) -> HttpResponse:
    vacancies = vacancy_storage.get_all_vacanies()
    context = {"vacancies": vacancies}
    return render(request=request, template_name="index.html", context=context)


def add_company(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request=request, template_name="company_add.html")
    elif request.method == "POST":
        name = request.POST["name"]
        employees_number = request.POST["employees_number"]

        company = Company(
            name=name,
            employees_number=employees_number
        )
        company_storage.add_company(company_to_add=company)
        return HttpResponseRedirect(redirect_to="/company/")


def company_list(request: HttpRequest) -> HttpResponse:
    companies = company_storage.get_all_companies()
    print(companies)
    context = {"companies": companies}
    return render(request=request, template_name="company_list.html", context=context)


def add_vacancy(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request=request, template_name="vacancy_add.html")
    elif request.method == "POST":
        name = request.POST["name"]
        company = request.POST["company"]
        level = request.POST["level"]
        expiriens = request.POST["expiriens"]
        min_salary = request.POST["min_salary"]
        max_salary = request.POST["max_salary"]

        vacancy = Vacancy(
            name=name,
            company=company,
            level=level,
            expiriens=expiriens,
            min_salary=min_salary,
            max_salary=max_salary
        )

        vacancy_storage.add_vacancy(vacancy_to_add=vacancy)
        return HttpResponseRedirect(redirect_to="/")
