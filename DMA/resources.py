from django.contrib.auth.models import User
from import_export import fields, widgets, resources
from DMA.models import MunicipalityDetails


class MunicipalityDetailsResource(resources.ModelResource):
    id = fields.Field(saves_null_values=False, column_name='id', attribute='id', widget=widgets.IntegerWidget())
    user = fields.Field(saves_null_values=True, column_name='user', attribute='user',
                        widget=widgets.ForeignKeyWidget(User, "username"))
    Sno = fields.Field(saves_null_values=False, column_name='Sno', attribute='Sno', widget=widgets.IntegerWidget())
    municipality_name = fields.Field(saves_null_values=True, column_name="municipality_name",
                                     attribute="municipality_name",
                                     widget=widgets.CharWidget())
    district = fields.Field(saves_null_values=True, column_name="district", attribute="district",
                            widget=widgets.CharWidget())
    region = fields.Field(saves_null_values=True, column_name="region", attribute="region",
                          widget=widgets.CharWidget())
    email_id1 = fields.Field(saves_null_values=True, column_name="email_id1", attribute="email_id1",
                             widget=widgets.CharWidget())
    email_id2 = fields.Field(saves_null_values=True, column_name="email_id2", attribute="email_id2",
                             widget=widgets.CharWidget())
    mc = fields.Field(saves_null_values=False, column_name='mc', attribute='mc', widget=widgets.IntegerWidget())
    me = fields.Field(saves_null_values=False, column_name='me', attribute='me', widget=widgets.IntegerWidget())

    class Meta:
        model = MunicipalityDetails
        fields = ('id', 'user', 'Sno', 'municipality_name', 'district', 'region',
                  'email_id1', 'email_id2', 'mc', 'me')
        clean_model_instances = True
