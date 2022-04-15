from import_export import fields, widgets, resources
from .models import *


class AgencyNameResource(resources.ModelResource):
    id = fields.Field(saves_null_values=False, column_name='id', attribute='id', widget=widgets.IntegerWidget())
    Pid = fields.Field(saves_null_values=False, column_name='Pid', attribute='Pid', widget=widgets.IntegerWidget())
    AgencyName = fields.Field(saves_null_values=True, column_name='AgencyName', attribute='AgencyName',
                              widget=widgets.CharWidget())
    AgencyType = fields.Field(saves_null_values=True, column_name='AgencyType', attribute='AgencyType',
                              widget=widgets.ForeignKeyWidget(AgencyType, 'AgencyType'))

    class Meta:
        model = AgencyName
        fields = ('id', 'Pid', "AgencyName", 'AgencyType')
        clean_model_instances = True


class DistrictResource(resources.ModelResource):
    id = fields.Field(saves_null_values=False, column_name='id', attribute='id', widget=widgets.IntegerWidget())
    Pid = fields.Field(saves_null_values=False, column_name='Pid', attribute='Pid', widget=widgets.IntegerWidget())
    District = fields.Field(saves_null_values=True, column_name='District', attribute='District',
                            widget=widgets.CharWidget())

    class Meta:
        model = District
        fields = ('id', 'Pid', 'District')
        clean_model_instances = True


class RegionResource(resources.ModelResource):
    id = fields.Field(saves_null_values=False, column_name='id', attribute='id', widget=widgets.IntegerWidget())
    Pid = fields.Field(saves_null_values=False, column_name='Pid', attribute='Pid', widget=widgets.IntegerWidget())
    Region = fields.Field(saves_null_values=True, column_name='Region', attribute='Region',
                          widget=widgets.CharWidget())

    class Meta:
        model = Region
        fields = ('id', 'Pid', 'Region')
        clean_model_instances = True


class MasterSanctionResource(resources.ModelResource):
    id = fields.Field(saves_null_values=False, column_name='id', attribute='id', widget=widgets.IntegerWidget())
    SNo = fields.Field(saves_null_values=False, column_name='SNo', attribute='SNo', widget=widgets.IntegerWidget())
    AgencyType = fields.Field(saves_null_values=True, column_name='AgencyType', attribute='AgencyType',
                              widget=widgets.ForeignKeyWidget(AgencyType, "AgencyType"))
    AgencyName = fields.Field(saves_null_values=True, column_name='AgencyName', attribute='AgencyName',
                              widget=widgets.ForeignKeyWidget(AgencyName, "AgencyName"))
    District = fields.Field(saves_null_values=True, column_name="District", attribute="District",
                            widget=widgets.ForeignKeyWidget(District, "District"))
    Scheme = fields.Field(saves_null_values=True, column_name="Scheme", attribute="Scheme",
                          widget=widgets.ForeignKeyWidget(Scheme, "Scheme"))
    Sector = fields.Field(saves_null_values=True, column_name="Sector", attribute="Sector",
                          widget=widgets.CharWidget())
    zone = fields.Field(saves_null_values=False, column_name='zone', attribute='zone', widget=widgets.IntegerWidget())
    ProjectName = fields.Field(saves_null_values=True, column_name="ProjectName", attribute="ProjectName",
                               widget=widgets.CharWidget())
    Project_ID = fields.Field(saves_null_values=True, column_name="Project_ID", attribute="Project_ID",
                              widget=widgets.CharWidget())
    ProjectCost = fields.Field(saves_null_values=True, column_name="ProjectCost", attribute="ProjectCost",
                               widget=widgets.DecimalWidget())
    ProposedCostByULB = fields.Field(saves_null_values=True, column_name="ProposedCostByULB",
                                     attribute="ProposedCostByULB", widget=widgets.DecimalWidget())
    ApprovedProjectCost = fields.Field(saves_null_values=True, column_name="ApprovedProjectCost",
                                       attribute="ApprovedProjectCost", widget=widgets.DecimalWidget())
    SchemeShare = fields.Field(saves_null_values=True, column_name="SchemeShare",
                               attribute="SchemeShare", widget=widgets.DecimalWidget())
    ULBShare = fields.Field(saves_null_values=True, column_name="ULBShare",
                            attribute="ULBShare", widget=widgets.DecimalWidget())
    GoMeeting = fields.Field(saves_null_values=True, column_name="GoMeeting",
                             attribute="GoMeeting", widget=widgets.IntegerWidget())
    Date_AS = fields.Field(saves_null_values=True, column_name="Date_AS",
                           attribute="Date_AS", widget=widgets.DateWidget())

    class Meta:
        model = MasterSanctionForm
        fields = ('id', 'SNo', 'AgencyType', 'Agency_Name', 'District',
                  'Scheme', 'Sector', 'ProjectName', 'Project_ID', 'ProjectCost', 'ProposedCostByTufidco',
                  'ApprovedProjectCost', 'SchemeShare', 'ULBShare', 'GoMeeting', 'Date_AS')


class SRPMasterSanctionResource(resources.ModelResource):
    id = fields.Field(saves_null_values=False, column_name='id', attribute='id', widget=widgets.IntegerWidget())
    SNo = fields.Field(saves_null_values=False, column_name='SNo', attribute='SNo', widget=widgets.IntegerWidget())
    AgencyType = fields.Field(saves_null_values=True, column_name='AgencyType', attribute='AgencyType',
                              widget=widgets.ForeignKeyWidget(AgencyType, "AgencyType"))
    AgencyName = fields.Field(saves_null_values=True, column_name='AgencyName', attribute='AgencyName',
                              widget=widgets.ForeignKeyWidget(AgencyName, "AgencyName"))

    Project_ID = fields.Field(saves_null_values=True, column_name="Project_ID", attribute="Project_ID",
                              widget=widgets.CharWidget())
    ProjectCost = fields.Field(saves_null_values=True, column_name="ProjectCost", attribute="ProjectCost",
                               widget=widgets.DecimalWidget())
    R1_Date = fields.Field(saves_null_values=True, column_name="R1_Date",
                           attribute="R1_Date", widget=widgets.DateWidget())
    R1_Amount = fields.Field(saves_null_values=True, column_name="R1_Amount", attribute="R1_Amount",
                             widget=widgets.DecimalWidget())
    R2_Date = fields.Field(saves_null_values=True, column_name="R2_Date",
                           attribute="R2_Date", widget=widgets.DateWidget())
    R2_Amount = fields.Field(saves_null_values=True, column_name="R2_Amount", attribute="R2_Amount",
                             widget=widgets.DecimalWidget())
    Balance = fields.Field(saves_null_values=True, column_name="Balance", attribute="Balance",
                           widget=widgets.DecimalWidget())
    Dropped = fields.Field(saves_null_values=True, column_name="Dropped", attribute="Dropped",
                           widget=widgets.DecimalWidget())
    BalanceEligible = fields.Field(saves_null_values=True, column_name="BalanceEligible", attribute="BalanceEligible",
                                   widget=widgets.DecimalWidget())

    class Meta:
        model = SRPMasterSanctionForm
        fields = ('id', 'SNo', 'AgencyType', 'Agency_Name',
                   'Project_ID', 'ProjectCost', 'SchemeShare', 'R1_Date', 'R1_Amount',
                  'R2_Date', 'R2_Amount', 'R_Total', 'Balance', 'Dropped', 'BalanceEligible')
