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
