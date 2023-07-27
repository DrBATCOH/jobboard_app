from django.db import migrations
from typing import Any
from core.models import Expirience

DEFAULT_EXPIRIENCE = (
        "Without experience",
        "Up to 1 year",
        "1 to 2 years",
        "2 to 3 years",
        "3 to 4 years",
        "4 to 5 years",
        "over 5 years",
)


def populate_expirience_table(apps: Any, schema_editor: Any) -> None:
    for expi in DEFAULT_EXPIRIENCE:
        Expirience.objects.create(name=expi)

def reverse_table_population(apps: Any, schema_editor: Any) -> None:
    for expi in DEFAULT_EXPIRIENCE:
        Expirience.objects.get(name=expi).delete()
    

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_expirience_alter_vacancy_expirience'),
    ]

    operations = [
        migrations.RunPython(
            code=populate_expirience_table,
            reverse_code=reverse_table_population,
        )

    ]