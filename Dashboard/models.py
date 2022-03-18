from django.db import models
from TUFIDCOapp.models import *


# Create your models here.
class Dashboard(MasterSanctionForm):
    class Meta:
        proxy = True
        verbose_name = "Dashboard"
        verbose_name_plural = "Dashboard"
