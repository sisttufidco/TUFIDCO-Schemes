from django.db import models
from TUFIDCOapp.models import *


# Create your models here.
class KNMTDashboard(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "KNMT"
        verbose_name_plural = "KNMT"

class KNMTDashboardR2122(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "KNMT (2021-2022)"
        verbose_name_plural = "KNMT (2021-2022)"

class KNMTDashboardR2223(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "KNMT (2022-2023)"
        verbose_name_plural = "KNMT (2022-2023)"


class SingaraChennaiDashboard(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "Singara Chennai 2.0"
        verbose_name_plural = "Singara Chennai 2.0"
