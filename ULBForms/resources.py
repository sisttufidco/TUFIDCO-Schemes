from import_export import fields, widgets, resources
from .models import *


class AgencyBankDetailsResources(resources.ModelResource):
    id = fields.Field(saves_null_values=False, column_name='id', attribute='id', widget=widgets.IntegerWidget())
    user = fields.Field(saves_null_values=True, column_name='user', attribute='user',
                        widget=widgets.ForeignKeyWidget(User, "username"))
    beneficiary_name = fields.Field(saves_null_values=True, column_name='beneficiary_name',
                                    attribute='beneficiary_name',
                                    widget=widgets.CharWidget())
    bank_name = fields.Field(saves_null_values=True, column_name='bank_name', attribute='bank_name',
                             widget=widgets.CharWidget())
    branch = fields.Field(saves_null_values=True, column_name='branch', attribute='branch',
                          widget=widgets.CharWidget())
    account_number = fields.Field(saves_null_values=True, column_name='account_number', attribute='account_number',
                                  widget=widgets.CharWidget())
    IFSC_code = fields.Field(saves_null_values=True, column_name='IFSC_code', attribute='IFSC_code',
                             widget=widgets.CharWidget())
    ULBType = fields.Field(saves_null_values=True, column_name='ULBType', attribute='ULBType',
                           widget=widgets.CharWidget())

    class Meta:
        model = AgencyBankDetails
        clean_model_instances = True


class ULBPanCardResources(resources.ModelResource):
    id = fields.Field(saves_null_values=False, column_name='id', attribute='id', widget=widgets.IntegerWidget())
    user = fields.Field(saves_null_values=True, column_name='user', attribute='user',
                        widget=widgets.ForeignKeyWidget(User, "username"))
    name = fields.Field(saves_null_values=True, column_name='name', attribute='name', widget=widgets.CharWidget())
    ULBType = fields.Field(saves_null_values=True, column_name='ULBType', attribute='ULBType',
                           widget=widgets.CharWidget())

    class Meta:
        model = ULBPanCard
        clean_model_instances = True


class AgencyProgressResource(resources.ModelResource):
    id = fields.Field(saves_null_values=False, column_name='id', attribute='id', widget=widgets.IntegerWidget())
    ULBName = fields.Field(saves_null_values=True, column_name='ULBName', attribute='ULBName',
                           widget=widgets.CharWidget())
    ULBType = fields.Field(saves_null_values=True, column_name='ULBType', attribute='ULBType',
                           widget=widgets.CharWidget())
    Scheme = fields.Field(saves_null_values=True, column_name='Scheme', attribute='Scheme',
                          widget=widgets.CharWidget())
    Sector = fields.Field(saves_null_values=True, column_name='Sector', attribute='Sector',
                          widget=widgets.CharWidget())
    Project_ID = fields.Field(saves_null_values=True, column_name='Project_ID', attribute='Project_ID',
                              widget=widgets.CharWidget())
    ProjectName = fields.Field(saves_null_values=True, column_name='ProjectName', attribute='ProjectName',
                               widget=widgets.CharWidget())
    Latitude = fields.Field(saves_null_values=True, column_name='Latitude', attribute='Latitude',
                            widget=widgets.CharWidget())
    Longitude = fields.Field(saves_null_values=True, column_name='Longitude', attribute='Longitude',
                             widget=widgets.CharWidget())
    PhysicalProgress = fields.Field(saves_null_values=True, column_name='PhysicalProgress',
                                    attribute='PhysicalProgress',
                                    widget=widgets.CharWidget())
    status = fields.Field(saves_null_values=True, column_name='status', attribute='status',
                          widget=widgets.CharWidget())
    nc_status = fields.Field(saves_null_values=True, column_name='nc_status', attribute='nc_status',
                             widget=widgets.CharWidget())
    Expenditure = fields.Field(saves_null_values=True, column_name='Expenditure', attribute='Expenditure',
                               widget=widgets.DecimalWidget())
    FundRelease = fields.Field(saves_null_values=True, column_name='FundRelease', attribute='FundRelease',
                               widget=widgets.DecimalWidget())
    valueofworkdone = fields.Field(saves_null_values=True, column_name='valueofworkdone', attribute='valueofworkdone',
                                   widget=widgets.DecimalWidget())
    percentageofworkdone = fields.Field(saves_null_values=True, column_name='percentageofworkdone',
                                        attribute='percentageofworkdone',
                                        widget=widgets.DecimalWidget())
    date_and_time = fields.Field(saves_null_values=True, column_name='date_and_time', attribute='date_and_time',
                                 widget=widgets.DateTimeWidget())

    class Meta:
        model = AgencyProgressModel
        fields = ('id', 'ULBName', 'ULBType', 'Scheme', 'Sector', 'Project_ID', 'ProjectName',
                  'Latitude', 'Longitude', 'PhysicalProgress', 'status', 'nc_status',
                  'Expenditure', 'FundRelease', 'valueofworkdone', 'percentageofworkdone', 'date_and_time')
        clean_model_instances = True


class AgencySanctionResource(resources.ModelResource):
    id = fields.Field(saves_null_values=False, column_name='id', attribute='id', widget=widgets.IntegerWidget())
    ULBName = fields.Field(saves_null_values=True, column_name='ULBName', attribute='ULBName',
                           widget=widgets.CharWidget())
    ULBType = fields.Field(saves_null_values=True, column_name='ULBType', attribute='ULBType',
                           widget=widgets.CharWidget())
    Scheme = fields.Field(saves_null_values=True, column_name='Scheme', attribute='Scheme',
                          widget=widgets.CharWidget())
    Sector = fields.Field(saves_null_values=True, column_name='Sector', attribute='Sector',
                          widget=widgets.CharWidget())
    Project_ID = fields.Field(saves_null_values=True, column_name='Project_ID', attribute='Project_ID',
                              widget=widgets.CharWidget())
    ProjectName = fields.Field(saves_null_values=True, column_name='ProjectName', attribute='ProjectName',
                               widget=widgets.CharWidget())
    ts_awarded = fields.Field(saves_null_values=True, column_name='ts_awarded', attribute='ts_awarded')
    tsrefno = fields.Field(saves_null_values=True, column_name='tsrefno', attribute='tsrefno',
                           widget=widgets.CharWidget())
    tsdate = fields.Field(saves_null_values=True, column_name='tsdate', attribute='tsdate',
                          widget=widgets.DateWidget())
    tr_awarded = fields.Field(saves_null_values=True, column_name='tr_awarded', attribute='tr_awarded',
                              widget=widgets.CharWidget())
    tawddate = fields.Field(saves_null_values=True, column_name='tawddate', attribute='tawddate',
                            widget=widgets.DateWidget())
    wd_awarded = fields.Field(saves_null_values=True, column_name='wd_awarded', attribute='wd_awarded',
                              widget=widgets.CharWidget())
    wdawddate = fields.Field(saves_null_values=True, column_name='wdawddate', attribute='wdawddate',
                            widget=widgets.DateWidget())
    work_awarded_amount1 = fields.Field(saves_null_values=True, column_name='work_awarded_amount1',
                                        attribute='work_awarded_amount1',
                                        widget=widgets.DecimalWidget())
    work_awarded_amount2 = fields.Field(saves_null_values=True, column_name='work_awarded_amount2',
                                        attribute='work_awarded_amount2',
                                        widget=widgets.DecimalWidget())
    date_and_time = fields.Field(saves_null_values=True, column_name='date_and_time',
                                        attribute='date_and_time',
                                        widget=widgets.DateTimeWidget())

    class Meta:
        model = AgencySanctionModel
        fields = (
            'id', 'ULBName', 'ULBType', 'Scheme', 'Sector', 'Project_ID', 'ProjectName',
            'ts_awarded', 'tsrefno', 'tsdate', 'tr_awarded', 'tawddate', 'wd_awarded',
            'wdawddate', 'work_awarded_amount1', 'work_awarded_amount2', 'date_and_time'
        )
        clean_model_instances = True