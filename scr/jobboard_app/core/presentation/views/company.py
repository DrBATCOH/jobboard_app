from __future__ import annotations
from typing import TYPE_CHECKING

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods


if TYPE_CHECKING:
    from django.http import HttpRequest

from core.presentation.forms import AddCompanyForm
from core.business_logic.services import create_company, get_companies, get_company_by_id
from core.business_logic.dto import AddCompanyDTO
from core.presentation.converters import convert_data_from_form_to_dto


@require_http_methods(request_method_list=["GET", "POST"])
def add_company(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = AddCompanyForm()
        context = {"form": form}
        return render(request=request, template_name="company_add.html", context=context)
    elif request.method == "POST":
        form = AddCompanyForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            data = convert_data_from_form_to_dto(AddCompanyDTO, form.cleaned_data)
            create_company(data=data)

        return HttpResponseRedirect(redirect_to=reverse("company_list"))


@require_http_methods(request_method_list=["GET"])
def company_list(request: HttpRequest) -> HttpResponse:
    companies = get_companies()
    context = {"companies": companies}
    return render(request=request, template_name="company_list.html", context=context)


@require_http_methods(request_method_list=["GET"])
def get_company(request: HttpRequest, company_id: int) -> HttpResponse:
    company = get_company_by_id(company_id=company_id)
    context = {"company": company}
    return render(request=request, template_name="get_company.html", context=context)
