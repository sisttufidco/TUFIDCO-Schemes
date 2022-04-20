from django.shortcuts import render
import xlwt
from django.http import HttpResponse

# Create your views here.
from ULBForms.models import AgencyProgressModel

CSRF_COOKIE_SECURE = True


def bus_export_tobecommenced_xls(request):
    global d
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="bus.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ToBeCommenced')
    row_num = 0



    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Reason', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'nc_status').filter(
        District=request.POST['district']).filter(status='Not Commenced').filter(Scheme='KNMT').filter(Sector='Bus Stand')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def btroad_export_tobecommenced_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="btroad.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ToBeCommenced')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Reason', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'nc_status').filter(
        District=request.POST['district']).filter(status='Not Commenced').filter(Scheme='KNMT').filter(Sector='BT Road')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def ccroad_export_tobecommenced_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="ccroad.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ToBeCommenced')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Reason', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'nc_status').filter(
        District=request.POST['district']).filter(status='Not Commenced').filter(Scheme='KNMT').filter(Sector='CC Road')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def ch_export_tobecommenced_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="CommunityHall.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ToBeCommenced')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Reason', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'nc_status').filter(
        District=request.POST['district']).filter(status='Not Commenced').filter(Scheme='KNMT').filter(
        Sector='Community Hall')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def cr_export_tobecommenced_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Crematorium.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ToBeCommenced')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Reason', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'nc_status').filter(
        District=request.POST['district']).filter(status='Not Commenced').filter(Scheme='KNMT').filter(
        Sector='Crematorium')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def cl_export_tobecommenced_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="culvert.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ToBeCommenced')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Reason', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'nc_status').filter(
        District=request.POST['district']).filter(status='Not Commenced').filter(Scheme='KNMT').filter(Sector='Culvert')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def kc_export_tobecommenced_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="knowledgecentre.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ToBeCommenced')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Reason', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'nc_status').filter(
        District=request.POST['district']).filter(status='Not Commenced').filter(Scheme='KNMT').filter(Sector='Knowledge Centre')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def mt_export_tobecommenced_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="market.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ToBeCommenced')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Reason', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'nc_status').filter(
        District=request.POST['district']).filter(status='Not Commenced').filter(Scheme='KNMT').filter(Sector='Market')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
def mbcb_export_tobecommenced_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="mbcb.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ToBeCommenced')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Reason', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'nc_status').filter(
        District=request.POST['district']).filter(status='Not Commenced').filter(Scheme='KNMT').filter(Sector='Metal Beam Crash Barriers')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def pk_export_tobecommenced_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="parks.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ToBeCommenced')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Reason', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'nc_status').filter(
        District=request.POST['district']).filter(status='Not Commenced').filter(Scheme='KNMT').filter(Sector='Parks')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def pb_export_tobecommenced_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="paverblock.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ToBeCommenced')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Reason', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'nc_status').filter(
        District=request.POST['district']).filter(status='Not Commenced').filter(Scheme='KNMT').filter(Sector='Paver Block')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def rw_export_tobecommenced_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="retainingwall.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ToBeCommenced')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Reason', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'nc_status').filter(
        District=request.POST['district']).filter(status='Not Commenced').filter(Scheme='KNMT').filter(Sector='Retaining wall')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def swm_export_tobecommenced_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="swm.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ToBeCommenced')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Reason', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'nc_status').filter(
        District=request.POST['district']).filter(status='Not Commenced').filter(Scheme='KNMT').filter(Sector='Solid Waste Mgt.')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def swd_export_tobecommenced_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="swd.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ToBeCommenced')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Reason', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'nc_status').filter(
        District=request.POST['district']).filter(status='Not Commenced').filter(Scheme='KNMT').filter(Sector='SWD')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def wb_export_tobecommenced_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="wb.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ToBeCommenced')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Reason', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'nc_status').filter(
        District=request.POST['district']).filter(status='Not Commenced').filter(Scheme='KNMT').filter(Sector='Water Bodies')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def btroad_export_progress_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="btroad.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('InProgress')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Percentage of Progress', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'percentageofworkdone').filter(Scheme='KNMT').filter(
        District=request.POST['district']).filter(status='In Progress').filter(Scheme='KNMT').filter(Sector='BT Road')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def swd_export_progress_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="swd.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('InProgress')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Percentage of Progress', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'percentageofworkdone').filter(Scheme='KNMT').filter(
        District=request.POST['district']).filter(status='In Progress').filter(Scheme='KNMT').filter(Sector='SWD')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def wb_export_progress_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="waterbodies.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('InProgress')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Percentage of Progress', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'percentageofworkdone').filter(Scheme='KNMT').filter(
        District=request.POST['district']).filter(status='In Progress').filter(Scheme='KNMT').filter(Sector='Water Bodies')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def rw_export_progress_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="retainingwall.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('InProgress')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Percentage of Progress', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'percentageofworkdone').filter(Scheme='KNMT').filter(
        District=request.POST['district']).filter(status='In Progress').filter(Scheme='KNMT').filter(Sector='Retaining wall')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def pb_export_progress_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="paverblock.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('InProgress')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Percentage of Progress', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'percentageofworkdone').filter(Scheme='KNMT').filter(
        District=request.POST['district']).filter(status='In Progress').filter(Scheme='KNMT').filter(Sector='Paver Block')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
def pk_export_progress_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="parks.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('InProgress')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Percentage of Progress', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'percentageofworkdone').filter(Scheme='KNMT').filter(
        District=request.POST['district']).filter(status='In Progress').filter(Scheme='KNMT').filter(Sector='Parks')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def mbcb_export_progress_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Metalbeamcrashbarrier.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('InProgress')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Percentage of Progress', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'percentageofworkdone').filter(Scheme='KNMT').filter(
        District=request.POST['district']).filter(status='In Progress').filter(Scheme='KNMT').filter(Sector='Metal Beam Crash Barriers')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def mt_export_progress_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="market.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('InProgress')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Percentage of Progress', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'percentageofworkdone').filter(Scheme='KNMT').filter(
        District=request.POST['district']).filter(status='In Progress').filter(Scheme='KNMT').filter(Sector='Market')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def kc_export_progress_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="knowledgecentre.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('InProgress')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Percentage of Progress', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'percentageofworkdone').filter(Scheme='KNMT').filter(
        District=request.POST['district']).filter(status='In Progress').filter(Scheme='KNMT').filter(Sector='Knowledge Centre')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
def bs_export_progress_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="busstand.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('InProgress')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Percentage of Progress', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'percentageofworkdone').filter(Scheme='KNMT').filter(
        District=request.POST['district']).filter(status='In Progress').filter(Scheme='KNMT').filter(Sector='Bus Stand')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def cc_export_progress_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="ccroad.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('InProgress')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Percentage of Progress', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'percentageofworkdone').filter(Scheme='KNMT').filter(
        District=request.POST['district']).filter(status='In Progress').filter(Scheme='KNMT').filter(Sector='CC Road')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def cr_export_progress_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="crematorium.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('InProgress')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Percentage of Progress', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'percentageofworkdone').filter(Scheme='KNMT').filter(
        District=request.POST['district']).filter(status='In Progress').filter(Scheme='KNMT').filter(Sector='Crematorium')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def cl_export_progress_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="culvert.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('InProgress')
    row_num = 0

    print(request.POST['district'])

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Percentage of Progress', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.values_list('District', 'ULBName', 'Project_ID', 'percentageofworkdone').filter(Scheme='KNMT').filter(
        District=request.POST['district']).filter(status='In Progress').filter(Scheme='KNMT').filter(Sector='Culvert')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response