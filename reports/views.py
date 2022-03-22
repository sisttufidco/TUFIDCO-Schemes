from django.shortcuts import render
import xlwt
from django.http import HttpResponse

# Create your views here.
from ULBForms.models import AgencyProgressModel
CSRF_COOKIE_SECURE = True


def park_export_xls(request):
    print('INSIDE')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="parks.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ToBeCommenced')
    row_num = 0
    d = request.POST['submit']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['District', 'ULB', 'Project ID', 'Reason', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = AgencyProgressModel.objects.filter(Scheme='KNMT').filter(Sector='Parks').filter(District=d).values_list(
        'District', 'ULBName', 'Project_ID', 'nc_status')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response