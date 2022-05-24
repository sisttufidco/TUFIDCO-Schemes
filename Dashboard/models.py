from django.db import models
from TUFIDCOapp.models import *


# Create your models here.
class KNMTDashboard(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "KNMT"
        verbose_name_plural = "KNMT"


class SingaraChennaiDashboard(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "Singara Chennai 2.0"
        verbose_name_plural = "Singara Chennai 2.0"