from django.urls import path
from . import views

urlpatterns = [
    path('export_bus', views.bus_export_tobecommenced_xls, name='export_bus'),
    path('export_btroad', views.btroad_export_tobecommenced_xls, name='export_bt'),
    path('export_ccroad', views.btroad_export_tobecommenced_xls, name='export_cc'),
    path('export_ch', views.ch_export_tobecommenced_xls, name='export_ch'),
    path('export_cr', views.cr_export_tobecommenced_xls, name='export_cr'),
    path('export_cl', views.cl_export_tobecommenced_xls, name='export_cl'),
    path('export_kc', views.kc_export_tobecommenced_xls, name='export_kc'),
    path('export_mt', views.mt_export_tobecommenced_xls, name='export_mt'),
    path('export_mbcb', views.mbcb_export_tobecommenced_xls, name='export_mbcb'),
    path('export_pk', views.pk_export_tobecommenced_xls, name='export_pk'),
    path('export_pb', views.pb_export_tobecommenced_xls, name='export_pb'),
    path('export_rw', views.rw_export_tobecommenced_xls, name='export_rw'),
    path('export_swm', views.swm_export_tobecommenced_xls, name='export_swm'),
    path('export_swd', views.swd_export_tobecommenced_xls, name='export_swd'),
    path('export_wb', views.wb_export_tobecommenced_xls, name='export_wb'),
]
