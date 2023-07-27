from __future__ import annotations

import timeit
from typing import TYPE_CHECKING

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.db import connection, transaction
from django.db.models import Count, F


if TYPE_CHECKING:
    from django.http import HttpRequest

from core.forms import (
    AddCompanyForm,
    AddVacancyForm,
    SearchVacancyForm
)
from core.models import (
    Company,
    Vacancy,
    Tag,
    Level
)


def print_queries():
    for q in connection.queries:
        print(q["sql"])


@require_http_methods(request_method_list=["GET"])
def index(request: HttpRequest) -> HttpResponse:
    filter_forms = SearchVacancyForm(request.GET)
    if filter_forms.is_valid():
        vacancies = Vacancy.objects.select_related("level", "company").prefetch_related("tags")
        form = SearchVacancyForm()
        context = {"vacancies": vacancies, "form": form}
        return render(request=request, template_name="index.html", context=context)
    else:
        context = {"vacancies": vacancies, "form": form}
        return render(request=request, template_name="index.html", context=context)

@require_http_methods(request_method_list=["GET", "POST"])
def add_company(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = AddCompanyForm()
        context = {"form": form}
        return render(
            request=request, template_name="company_add.html", context=context
        )

    elif request.method == "POST":
        form = AddCompanyForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            employees_number = form.cleaned_data["employees_number"]
            Company.objects.create(name=name, employees_number=employees_number)
        else:
            return HttpResponseBadRequest(content="Form validation failed.")
    return HttpResponseRedirect(redirect_to=reverse("company_list"))


@require_http_methods(request_method_list=["GET"])
def company_list(request: HttpRequest) -> HttpResponse:
    companies = Company.objects.annotate(vacancy__count=Count("vacancy__id")).order_by("-vacancy__count")
    print(list(companies))
    print_queries()
    context = {"companies": companies}
    return render(request=request, template_name="company_list.html", context=context)


@require_http_methods(request_method_list=["GET", "POST"])
def add_vacancy(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = AddVacancyForm()
        context = {"form": form}
        return render(
            request=request, template_name="vacancy_add.html", context=context
        )

    elif request.method == "POST":
        form = AddVacancyForm(data=request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            company_name = form.cleaned_data["company"]
            level_name = form.cleaned_data["level_name"]
            expirience = form.cleaned_data["expirience"]
            min_salary = form.cleaned_data["min_salary"]
            max_salary = form.cleaned_data["max_salary"]
            tags = form.cleaned_data["tags"]
            try:
                with transaction.atomic():
                    tags: list[str] = tags.split("\r\n")
                    tags_list: list[Tag] = []
                    for tag in tags:
                        tag = tag.lower()
                        try:
                            tags_from_db = Tag.objects.get(name=tag)
                        except Tag.DoesNotExist:
                            tags_from_db = Tag.objects.create(name=tag)
                        tags_list.append(tags_from_db)

                    level = Level.objects.get(name=level_name)
                    company = Company.objects.get(name=company_name)

                    created_vacancy = Vacancy.objects.create(
                        name=name,
                        company=company,
                        level=level,
                        expirience=expirience,
                        min_salary=min_salary,
                        max_salary=max_salary
                    )

                    created_vacancy.tags.set(tags_list)
            except Company.DoesNotExist:
                context = {"form":form}
                print_queries()
                return render(request=request, template_name="vacancy_add.html", context=context)

        else:
            context = {"form":form}
            return render(request=request, template_name="vacancy_add.html", context=context)
        return HttpResponseRedirect(redirect_to=reverse("index"))


@require_http_methods(request_method_list=["GET"])
def get_vacancy(request: HttpRequest, vacancy_id: int) -> HttpResponse:
    vacancy = Vacancy.objects.get(id=vacancy_id)
    context = {"vacancy": vacancy}
    return render(request=request, template_name="get_vacancy.html", context=context)


@require_http_methods(request_method_list=["GET"])
def get_company(request: HttpRequest, company_id: int) -> HttpResponse:
    company = Company.objects.get(id=company_id)
    context = {"company": company}
    return render(request=request, template_name="get_company.html", context=context)
