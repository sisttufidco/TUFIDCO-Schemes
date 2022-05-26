from django.db import models
from ULBForms.models import AgencyProgressModel, AgencySanctionModel
# Create your models here.

class MunicipalityCompletedProjects(AgencyProgressModel):
    class Meta:
        proxy = True
        verbose_name = "DMA Completed Projects"
        verbose_name_plural = "DMA Completed Projects"

class TownPanchayatCompletedProjects(AgencyProgressModel):
    class Meta:
        proxy = True
        verbose_name = "CTP Completed Projects"
        verbose_name_plural = "CTP Completed Projects"

class MunicipalityInProgressProjects(AgencyProgressModel):
    class Meta:
        proxy = True
        verbose_name = "DMA In Progress Projects"
        verbose_name_plural = "DMA In Progress Projects"

class TownPanchayatInProgressProjects(AgencyProgressModel):
    class Meta:
        proxy = True
        verbose_name = "CTP In Progress Projects"
        verbose_name_plural = "CTP In Progress Projects"

class MunicipalityNotCommencedProjects(AgencyProgressModel):
    class Meta:
        proxy = True
        verbose_name = "DMA Not Commenced Projects"
        verbose_name_plural = "DMA Not Commenced Projects"

class TownPanchayatNotCommencedProjects(AgencyProgressModel):
    class Meta:
        proxy = True
        verbose_name = "CTP Not Commenced Projects"
        verbose_name_plural = "CTP Not Commenced Projects"