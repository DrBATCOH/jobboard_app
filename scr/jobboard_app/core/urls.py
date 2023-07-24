from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("company/add/", add_company, name="company-add"),
    path("company/", company_list, name="company"),
    path("vacancy/add/", add_vacancy, name="vacancy-add"),
         
]